import time

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from prompts import SYSTEM_PROMPT

load_dotenv()

openai_client = OpenAI()

st.set_page_config(page_title="🔬 Prompt Evaluator")
st.title("🔬 Prompt Evaluator")

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    value=st.secrets.api_key.openai,
)
has_valid_openai_api_key = openai_api_key and openai_api_key.startswith("sk-")

if not has_valid_openai_api_key:
    st.warning("Please enter your OpenAI API key!", icon="⚠")

models_list = [
    "gpt-4",
    "gpt-3.5-turbo",
]
model_text = st.selectbox("Select the LLM:", models_list)

prompt_text = st.text_input(
    "Enter your prompt:",
    placeholder="Enter prompt here ...",
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model_text

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if (
    has_valid_openai_api_key
    and prompt_text != ""
    and model_text != ""
    and st.button("Evaluate")
):
    st.header("Evaluating ...")
    start_time = time.time()
    stream_response = openai_client.chat.completions.create(
        model=model_text,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text},
        ],
        temperature=0,
        stream=True,
    )
    response = st.write_stream(stream_response)
    # st.session_state.messages.append({"role": "assistant", "content": response})
    # st.success(response)
    # collected_chunks = []
    # collected_messages = []
    # for chunk in response:
    #     chunk_time = time.time() - start_time
    #     print(chunk)
    #     print(chunk.choices[0].delta.content)
    #     print("****************")
    #     collected_chunks.append(chunk)
    #     chunk_message = chunk.choices[0].delta.content
    #     collected_messages.append(chunk_message)
    #     print(
    #         f"Message received {chunk_time:.2f} seconds after request: {chunk_message}"
    #     )
