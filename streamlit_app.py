import streamlit as st
import requests

st.set_page_config(page_title="Multi-Agent Research Assistant")

st.title("🧠 Multi-Agent Research Assistant")

query = st.text_input("Enter your research question:")

if st.button("Run Research"):

    if not query:
        st.warning("Please enter a query")
    else:
        st.write("### 🔄 Processing...\n")

        response = requests.post(
            #"http://127.0.0.1:8000/research/stream",
            "http: // backend: 8000",
            json={"query": query},
            stream=True
        )

        output_box = st.empty()  # placeholder

        full_text = ""

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                decoded = chunk.decode("utf-8")
                full_text += decoded

                output_box.text(full_text)