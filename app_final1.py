# Improved code for app_final1.py

import os
import streamlit as st
from wordcloud import WordCloud
import requests

# Using environment variables for API keys
API_KEY = os.getenv('API_KEY')

# Proper AI system prompts and error handling
def get_ai_response(prompt):
    try:
        response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions',
                                  headers={'Authorization': f'Bearer {API_KEY}'},
                                  json={'prompt': prompt, 'max_tokens': 150})
        response.raise_for_status()  # Raises an error for bad responses
        return response.json()['choices'][0]['text']
    except Exception as e:
        st.error(f'Error obtaining AI response: {e}')
        return 'Error in AI response.'

# Wordcloud function for Streamlit
def generate_wordcloud(text):
    try:
        if text:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            return wordcloud
        else:
            st.warning('No text provided for wordcloud generation.')
            return None
    except Exception as e:
        st.error(f'Error generating wordcloud: {e}')
        return None

# Streamlit UI components
def main():
    st.title('AI Text Generator and Wordcloud Creator')
    user_input = st.text_area('Enter your prompt for the AI:')
    if st.button('Generate AI Response'): 
        ai_response = get_ai_response(user_input)
        st.subheader('AI Response:')
        st.write(ai_response)
        if ai_response:
            wordcloud = generate_wordcloud(ai_response)
            if wordcloud:
                st.image(wordcloud.to_array())

if __name__ == '__main__':
    main()
