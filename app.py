import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv('API_KEY')
st.set_page_config(initial_sidebar_state="expanded")
client = Groq(api_key=API_KEY)

st.markdown(
    "<h1 style='text-align: center;font-family: Arial'>Asistente IA Clinica SantaMaria</h1>",
    unsafe_allow_html=True
)


modelos = {
    'llama-3.1-8b': 'llama-3.1-8b-instant',
    'llama-3.3-70b': 'llama-3.3-70b-versatile',
    'gpt-oss-120b': 'openai/gpt-oss-120b',
    'gpt-oss-20b': 'openai/gpt-oss-20b'
}
st.sidebar.markdown('### Seleccione un modelo de IA')
modelo_nombre = st.sidebar.selectbox("", list(modelos.keys()))
modelo = modelos[modelo_nombre]


if 'messages_by_model' not in st.session_state:
    st.session_state.messages_by_model = {}


if modelo not in st.session_state.messages_by_model:
    st.session_state.messages_by_model[modelo] = []


messages = st.session_state.messages_by_model[modelo]


for message in messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


if prompt := st.chat_input('Escribe tu mensaje aquí'):
    with st.chat_message('user'):
        st.markdown(prompt)
    messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        try:
            stream = client.chat.completions.create(
                model=modelo,
                messages=[
                    {'role': 'system', 'content': 'Eres un asistente amable y servicial y saludaras asi:👋 ¡Hola! Bienvenido/a a Clinica dental SantaMaria, donde cuidamos tu sonrisa 😁.Soy el asistente virtual y estoy aquí para ayudarte. ¿En qué puedo asistirte hoy? Por favor, selecciona una opción: 1 Agendar una cita; 2 Consultar horarios o ubicación; 3 Servicios disponibles; 4 Hablar con un especialista; 5 Otras consultas.'},
                    *messages
                ],
                stream=True
            )

            full_response = ''
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    message_placeholder.markdown(full_response)

            messages.append({'role': 'assistant', 'content': full_response})

        except Exception as e:
            st.error(f'Error: {str(e)}')
st.sidebar.markdown('## Prompt utilizado')
st.sidebar.text('\n Eres un asistente amable y servicial y saludaras asi:\n\n👋 ¡Hola! Bienvenido/a a Clinica dental SantaMaria, donde cuidamos tu sonrisa 😁.\nSoy el asistente virtual y estoy aquí para ayudarte. ¿En qué puedo asistirte hoy? Por favor, selecciona una opción:\n\n1 Agendar una cita; \n2 Consultar horarios o ubicación; \n3 Servicios disponibles; \n4 Hablar con un especialista; \n5 Otras consultas.')