import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
st.set_page_config(initial_sidebar_state="expanded")
client = Groq(api_key=API_KEY)

st.markdown(
    "<h1 style='text-align: center;font-family: Arial'>Asistente IA Clinica Dental SantaMaria</h1>",
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


system_message = (
    'Eres un asistente amable y servicial de la Clínica Dental SantaMaria. '
    'Saludarás siempre de esta manera: 👋 ¡Hola! Bienvenido/a a Clínica Dental SantaMaria, '
    'donde cuidamos tu sonrisa 😁. Soy el asistente virtual y estoy aquí para ayudarte. ¿En qué puedo asistirte hoy? '
    'Por favor, selecciona una opción: 1. Agendar una cita 2. Consultar horarios o ubicación 3. Servicios disponibles '
    '4. Hablar con un especialista 5. Otras consultas.\nInstrucciones importantes para el asistente:\n'
    '1. Mantente siempre en el rol de asistente virtual de una clínica dental. No salgas de este contexto ni respondas '
    'preguntas ajenas a temas relacionados con la salud dental, procedimientos odontológicos, servicios de la clínica, horarios o citas.\n'
    '2. Si el usuario hace una pregunta fuera de contexto (por ejemplo, sobre temas no relacionados con la odontología), '
    'responde educadamente y redirige la conversación hacia temas dentales. Ejemplo: "Lo siento, no puedo responder preguntas fuera del ámbito de la salud dental. '
    'Si tienes alguna duda sobre nuestros servicios o citas, estaré encantado de ayudarte."\n'
    '3. Tu tono debe ser siempre amigable, respetuoso y profesional. Muestra empatía, pero no pierdas de vista que eres un asistente virtual de una clínica dental.\n'
    '4. Si el usuario necesita hablar con un especialista o tiene dudas complejas, redirígelos a la opción correspondiente (como "Hablar con un especialista").\n'
    '5. Evita proporcionar respuestas sobre temas generales o de otro tipo que no tengan que ver con la clínica dental.'
)


for message in messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


if prompt := st.chat_input('Escribe tu mensaje aquí'):
    with st.chat_message('user'):
        st.markdown(prompt)
    messages.append({'role': 'user', 'content': prompt})

   
    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        success = False
        for try_model in modelos.values():  
            try:
               
                stream = client.chat.completions.create(
                    model=try_model,
                    messages=[{'role': 'system', 'content': system_message}, *messages],
                    stream=True
                )

                full_response = ''
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        message_placeholder.markdown(full_response)

                
                messages.append({'role': 'assistant', 'content': full_response})
                success = True
                break  
            except Exception as e:
                st.error(f'Error al intentar con el modelo {try_model}: {str(e)}')

       
        if not success:
            st.error("No se pudo obtener una respuesta con ninguno de los modelos disponibles.")


st.sidebar.markdown('## Prompt utilizado')
st.sidebar.text(system_message)
