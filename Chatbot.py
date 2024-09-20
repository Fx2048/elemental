import openai
import streamlit as st

st.title("ChatGPT-like clone")

# Inicializa el cliente de OpenAI con la clave de API
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Muestra los mensajes existentes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Procesa la entrada del usuario
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Genera la respuesta del asistente
    with st.chat_message("assistant"):
        response = ""
        stream = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        for chunk in stream:
            response += chunk["choices"][0]["delta"]["content"]
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
