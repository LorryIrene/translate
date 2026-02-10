# -*- coding: utf-8 -*-
import hashlib
import time
import requests
import streamlit as st
from zhipuai import ZhipuAI
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# --- 1. 安全配置 ---
# 建议在本地创建 .env 文件或在 GitHub Secrets 中配置
# 这里尝试从环境变量读取，如果没有则提示用户输入
YOUDAO_APP_KEY = st.secrets.get("YOUDAO_APP_KEY")
YOUDAO_APP_SECRET = st.secrets.get("YOUDAO_APP_SECRET")
ZHIPU_API_KEY = st.secrets.get("ZHIPU_API_KEY")

# 初始化客户端
if ZHIPU_API_KEY:
    client = ZhipuAI(api_key=ZHIPU_API_KEY)
else:
    st.error("请配置 ZhipuAI API Key！")

# --- 2. 工具函数 ---

def addAuthParams(app_key, app_secret, params):
    salt = str(int(time.time() * 1000))
    curtime = str(int(time.time()))
    
    # 辅助函数：处理截取
    q = params.get('q', '')
    size = len(q)
    input_str = q if size <= 20 else q[:10] + str(size) + q[-10:]
    
    sign_str = app_key + input_str + salt + curtime + app_secret
    sign = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()

    params.update({
        'appKey': app_key,
        'salt': salt,
        'curtime': curtime,
        'sign': sign,
        'signType': 'v3'
    })

def create_translation(text, lang_from, lang_to):
    """调用有道翻译 API"""
    data = {'q': text, 'from': lang_from, 'to': lang_to}
    addAuthParams(YOUDAO_APP_KEY, YOUDAO_APP_SECRET, data)
    
    try:
        res = requests.post('https://openapi.youdao.com/api', data=data, timeout=10)
        return res.json()
    except Exception as e:
        st.error(f"翻译请求失败: {e}")
        return None

def correct_sentence_ai(user_sentence):
    """
    通过 System Prompt 提高 AI 调用的准确性，
    确保它只返回纠正后的结果。
    """
    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "system", "content": "你是一个专业的语言老师。请直接返回用户句子的纠正版本，不要有任何解释或开场白。如果句子已经正确，请原样返回。"},
                {"role": "user", "content": f"纠正这个句子: {user_sentence}"}
            ],
            temperature=0.1,  # 降低随机性，提高稳定性
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"AI 纠错失败: {e}")
        return user_sentence

def display_wordcloud(text):
    """生成并返回词云图表对象"""
    # 增加中文字体支持（如果需要）
    wc = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        font_path='simhei.ttf' if os.path.exists('simhei.ttf') else None 
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    return fig

# --- 3. Streamlit UI ---

def main():
    st.set_page_config(page_title="语言学习助手", layout="centered")
    st.title("🌟 语言学习辅助工具")
    st.markdown("输入任何句子，AI 将为您纠正语法并完成翻译。")

    # 侧边栏配置
    with st.sidebar:
        st.header("设置")
        lang_options = {
            "自动检测": "auto", "中文": "zh-CHS", "英语": "en", 
            "日语": "ja", "韩语": "ko", "法语": "fr"
        }
        lang_from = st.selectbox("源语言", list(lang_options.keys()), index=0)
        lang_to = st.selectbox("目标语言", list(lang_options.keys()), index=2)

    user_sentence = st.text_area("请输入您想要纠正的句子：", placeholder="e.g. He go to school yesterday.")

    if st.button("开始纠正与翻译", type="primary"):
        if not user_sentence.strip():
            st.warning("请输入有效内容。")
            return

        with st.spinner("处理中..."):
            # 1. AI 纠错
            corrected = correct_sentence_ai(user_sentence)
            
            col1, col2 = st.columns(2)
            with col1:
                st.info("### 原始句子")
                st.write(user_sentence)
            with col2:
                st.success("### 纠正结果")
                st.write(corrected)

            # 2. 翻译
            trans_res = create_translation(corrected, lang_options[lang_from], lang_options[lang_to])
            if trans_res and 'translation' in trans_res:
                st.markdown("---")
                st.subheader("🌐 翻译结果")
                st.write(trans_res['translation'][0])

            # 3. 可视化分析
            st.markdown("---")
            tab1, tab2 = st.tabs(["📊 长度对比", "☁️ 词云图"])
            
            with tab1:
                lengths = {"原始": len(user_sentence), "纠正后": len(corrected)}
                st.bar_chart(lengths)
            
            with tab2:
                st.pyplot(display_wordcloud(corrected))

if __name__ == "__main__":
    main()
