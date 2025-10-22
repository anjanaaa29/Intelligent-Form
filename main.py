import streamlit as st
import tempfile
import os
from src.extract import extract_multiple_forms
from src.summary import generate_summary, generate_holistic_summary
from src.qa import answer_question

# Streamlit App Config
st.set_page_config(page_title="🧠 Intelligent Form Agent", layout="wide")

st.title("🧾 Intelligent Form Agent")
st.write("Upload one or more PDF, DOCX, or image forms to extract, summarize, and ask questions.")

# File Upload Section
uploaded_files = st.file_uploader(
    "Upload your form files",
    type=["pdf", "docx", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"Processing {len(uploaded_files)} file(s)... Please wait.")

    # Save uploaded files temporarily
    temp_files = []
    for file in uploaded_files:
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, file.name)
        with open(temp_path, "wb") as f:
            f.write(file.read())
        temp_files.append(temp_path)

    # Extract text
    with st.spinner("Extracting text..."):
        results = extract_multiple_forms(temp_files)

    # Generate summaries for each file
    summaries = {}
    for file_path, text in results.items():
        if not text.strip():
            st.error(f"❌ No text extracted from {os.path.basename(file_path)}")
            continue

        st.subheader(f"📄 {os.path.basename(file_path)}")
        with st.spinner("Generating summary..."):
            summary = generate_summary(text)
            summaries[file_path] = summary
            st.success("✅ Summary generated")
            with st.expander("View Summary"):
                st.write(summary)

    # Generate Holistic Summary (if multiple files uploaded)
    if len(results) > 1:
        st.markdown("---")
        st.subheader("🌐 Holistic Summary Across All Forms")
        with st.spinner("Generating holistic summary..."):
            holistic_summary = generate_holistic_summary(results)
            st.success("✅ Holistic summary generated successfully")
            st.write(holistic_summary)

    # Q&A Section
    st.markdown("---")
    question = st.text_input("💬 Ask a question about the forms:")
    if question:
        st.subheader("🧠 Answers")
        for file_path, text in results.items():
            if not text.strip():
                continue
            answer = answer_question(text, question)
            st.markdown(f"**{os.path.basename(file_path)}:** {answer}")

else:
    st.info("👆 Upload one or more files to begin.")
