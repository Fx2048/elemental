import os
from groq import Groq  # Importar la librería de GroqCloud
import streamlit as st

# Crear la barra lateral para ingresar la clave API
with st.sidebar:
    groq_api_key = st.text_input("GroqCloud API Key", key="chatbot_api_key", type="password")
    "[Get a GroqCloud API key](https://groqcloud.com/account/api-keys)"  # Cambia el enlace al correspondiente de GroqCloud
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by GroqCloud")

# Inicializar la sesión de mensajes si no existe
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Mostrar los mensajes previos en el chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Capturar el input del usuario
if prompt := st.chat_input():
    if not groq_api_key:
        st.info("Please add your GroqCloud API key to continue.")
        st.stop()

    # Inicializar el cliente de GroqCloud
    client = Groq(api_key=groq_api_key)
    
    # Agregar el mensaje del usuario a la sesión de mensajes
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Realizar la solicitud a la API de GroqCloud para obtener la respuesta
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",  # Cambia al modelo que desees usar en GroqCloud
        messages=st.session_state["messages"]
    )

    # Obtener el contenido de la respuesta
    msg = response.choices[0].message.content
    
    # Agregar el mensaje del asistente a la sesión de mensajes
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

