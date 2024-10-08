import streamlit as st
from groq import Groq, GroqError

# Configurar la clave API en la barra lateral
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", key="file_qa_api_key", type="password")
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 File Q&A with Groq")

# Subir archivo de texto
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))

# Pregunta relacionada al archivo
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

# Verificar si hay archivo, pregunta y clave API
if uploaded_file and question and not groq_api_key:
    st.info("Please add your Groq API key to continue.")
    st.stop()

if uploaded_file and question and groq_api_key:
    # Leer el archivo y decodificarlo
    article = uploaded_file.read().decode()

    # Construir el prompt que se enviará a la API de Groq
    prompt = f"""Here is an article:\n\n{article}\n\nQuestion: {question}"""

    # Inicializar el cliente de Groq con la clave API
    client = Groq(api_key=groq_api_key)

    try:
        # Realizar la solicitud a la API de Groq
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Cambia el modelo si es necesario
            messages=[{"role": "user", "content": prompt}]
        )

        # Acceder al contenido de la respuesta generada
        completion_text = response.choices[0].message.content

        # Mostrar la respuesta en la interfaz de Streamlit
        st.write("### Answer")
        st.write(completion_text)

    except GroqError as e:
        # Manejar posibles errores al hacer la solicitud
        st.error(f"Error en la solicitud: {e}")

