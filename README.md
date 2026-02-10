🌟 Language Learning Assistant (语言学习辅助工具)
这是一个基于 Streamlit 开发的轻量级语言学习工具。它结合了 智谱 AI (GLM-4) 的强大纠错能力和 有道翻译 API 的精准翻译，旨在帮助用户纠正外语语法错误并实时获取翻译参考。

✨ 主要功能
智能纠错：利用 GLM-4 模型对输入的句子进行语法检查和自然语言优化。

多语种翻译：支持中、英、日、韩、法、德等多种语言的互译。

可视化分析：

词云生成：直观展示纠正后句子的关键词权重。

长度对比：通过图表直观对比原始句子与纠正后句子的字数差异。

响应式界面：基于 Streamlit 构建，支持 PC 和移动端访问。

🚀 快速开始
1. 克隆仓库
Bash

git clone https://github.com/你的用户名/your-repo-name.git
cd your-repo-name
2. 安装依赖
确保你已安装 Python 3.8+，然后运行：

Bash

pip install -r requirements.txt
3. 配置 API 密钥
为了安全起见，本项目使用 Streamlit 的 secrets 管理机制。请在项目根目录下创建 .streamlit/secrets.toml 文件，并填入你的密钥：

Ini, TOML

# .streamlit/secrets.toml
YOUDAO_APP_KEY = "你的有道智云 APP KEY"
YOUDAO_APP_SECRET = "你的有道智云 APP SECRET"
ZHIPU_API_KEY = "你的智谱AI API KEY"
注意：.streamlit/ 目录已被列入 .gitignore，请勿将其上传到公开仓库。

4. 运行应用
Bash

streamlit run app_final1.py
🛠️ 技术栈
Frontend: Streamlit

LLM API: Zhipu AI (BigModel)

Translation API: Youdao AI Cloud

Data Viz: Matplotlib, WordCloud

📝 开源协议
本项目采用 MIT License 开源。
