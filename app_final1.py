# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 01:40:37 2024

@author: penumbra
"""

import hashlib
import time
import requests
import streamlit as st
from zhipuai import ZhipuAI
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Your Youdao API credentials
APP_KEY = '6f4a111b1b6a7962'
APP_SECRET = 'n02iZRpvBPL6KOUg1QLfF3u8SerKE4WQ'

# Your Zhipu AI API key
API_KEY = "8047d68f1cf1994bce6d2d150d1f2546.Wu8ryeDgpsit0ajR"
client = ZhipuAI(api_key=API_KEY)

def addAuthParams(app_key, app_secret, params):
    """
    添加认证参数到请求中。
    """
    salt = str(int(time.time() * 1000))
    curtime = str(int(time.time()))
    sign_str = app_key + truncate(params['q']) + salt + curtime + app_secret
    sign = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()

    # 添加认证参数
    params['appKey'] = app_key
    params['salt'] = salt
    params['curtime'] = curtime
    params['sign'] = sign
    params['signType'] = 'v3'
    
def truncate(q):
    """
    进行字符串截取
    """
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[:10] + str(size) + q[-10:]

def createRequest(text, lang_from, lang_to):
    '''
    Create a request to translate the corrected text
    '''
    vocab_id = ''  # Your user vocab ID, if any

    data = {'q': text, 'from': lang_from, 'to': lang_to, 'vocabId': vocab_id}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    return res.json()

def doCall(url, header, params, method):
    if 'get' == method:
        response = requests.get(url, params=params, headers=header)
    elif 'post' == method:
        response = requests.post(url, data=params, headers=header)
    else:
        raise ValueError("Invalid HTTP method specified: {}".format(method))
    
    return response

def correct_sentence(user_sentence):
    # 使用智谱 AI 的文本校正功能来帮助用户纠正句子
    messages = [
        {
            "role": "user",
            "content": user_sentence
        }
    ]
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages
    )
    return response.choices[0].message.content

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Streamlit 应用程序的主入口点
def main():
    st.title("语言学习辅助")

    # 用户输入句子
    user_sentence = st.text_input("请输入您想要纠正的句子：")

    # 源语言和目标语言选择
    lang_from = st.selectbox("选择源语言", ["auto", "zh-CHS", "en", "ja", "ko", "fr", "de", "ru", "es", "pt", "it", "vi"])
    lang_to = st.selectbox("选择目标语言", ["zh-CHS", "en", "ja", "ko", "fr", "de", "ru", "es", "pt", "it", "vi"])

    # 当用户提交句子时，显示纠正后的句子并翻译
    if st.button("纠正并翻译句子"):
        if user_sentence:
            corrected_sentence = correct_sentence(user_sentence)
            st.write(f"纠正后的句子：{corrected_sentence}")

            # 生成词云
            st.subheader("纠正后的句子词云")
            st.pyplot(generate_wordcloud(corrected_sentence))

            # 翻译句子
            translation_response = createRequest(corrected_sentence, lang_from, lang_to)
            translation = translation_response.get('translation', [''])[0]
            st.write(f"翻译后的句子：{translation}")

            # 显示原始句子和纠正句子的长度
            st.subheader("句子长度比较")
            lengths = {"Original": len(user_sentence), "Corrected": len(corrected_sentence)}
            st.bar_chart(lengths)

        else:
            st.write("请输入一个句子。")

if __name__ == "__main__":
    main()
