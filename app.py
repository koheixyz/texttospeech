import os
from google.oauth2.service_account import Credentials
from google.cloud import texttospeech
import io
import streamlit as st

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './secret.json'

def synthesize_speech(text, lang, gender):
    
    gender_type = {
        '男性': texttospeech.SsmlVoiceGender.MALE,
        '女性': texttospeech.SsmlVoiceGender.FEMALE
    }

    lang_code = {
        '英語': 'en-US',
        '日本語': 'ja-JP'
    }

    name_type = {
        '男性': 'ja-JP-Wavenet-D',
        '女性': 'ja-JP-Neural2-B'
    }

    credentials = Credentials.from_service_account_info(
        # secrets.toml
        st.secrets["APPLICATION_CREDENTIALS"],
    )

    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        name = name_type[gender],
        language_code = lang_code[lang],
        ssml_gender=gender_type[gender]
    )

    if gender == '男性':
        speaking_rate = 0.5
    else:
        speaking_rate = 1.75
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate = speaking_rate
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response

st.title('テキストを音声に変換してみる')

st.markdown('### まずは準備')

input_option = st.selectbox(
    'テキストの選択',
    ('キーボード', 'ファイル')
)
input_data = None

if input_option == 'キーボード':
    input_data = st.text_area(
        '入力して',
        '猪木の名言。元気が一番、元気があれば何でもできる！'
    )
else:
    uploaded_file = st.file_uploader('テキストファイルをアップロード',['txt'])
    if uploaded_file:
        content = uploaded_file.read()
        input_data = content.decode()

if input_data:
    st.markdown('### 音声の設定')

    lang = st.selectbox(
        '言語を選択して',
        ('日本語', '英語')
    )

    gender = st.selectbox(
        '性別を選択して',
        ('男性', '女性')
    )

    if st.button('OK'):
        response = synthesize_speech(input_data, lang, gender)
        st.audio(response.audio_content)









