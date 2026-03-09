import streamlit as st
import requests

API_URL = "http://localhost:8010"

st.set_page_config(page_title="Personal AI Assistant", layout="wide")

st.title("🤖 Personal AI Assistant")

# ----------------------------------------------------
# LAYOUT
# ----------------------------------------------------

col1, col2, col3 = st.columns([1.2,2.5,1.2])


# ----------------------------------------------------
# DOCUMENT PANEL
# ----------------------------------------------------

with col1:

    st.header("📂 Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key="pdf_uploader"
    )

    if st.button("Upload Document", key="upload_btn"):

        if uploaded_file is None:

            st.warning("Please select a PDF file")

        else:

            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }

            with st.spinner("Uploading and processing document..."):

                try:

                    res = requests.post(
                        f"{API_URL}/api/documents/upload",
                        files=files
                    )

                    if res.status_code == 200:

                        data = res.json()

                        if data.get("status") == "success":
                            st.success(data.get("message", "Upload successful"))

                        else:
                            st.error("Upload failed")
                            st.write(data)

                    else:
                        st.error(f"Upload failed: {res.status_code}")
                        st.write(res.text)

                except Exception as e:

                    st.error("Backend connection failed")
                    st.write(e)

    st.divider()

    # ----------------------------------------------------
    # DOCUMENT LIST
    # ----------------------------------------------------

    st.subheader("Stored Documents")

    documents = []

    try:

        res = requests.get(f"{API_URL}/api/documents/list")

        if res.status_code == 200:

            data = res.json()

            documents = data.get("documents", [])

    except Exception as e:

        st.error("Backend not reachable")
        st.write(e)

    selected_docs = []

    for i, doc in enumerate(documents):

        if isinstance(doc, dict):
            doc_name = doc.get("name", "unknown")
        else:
            doc_name = doc

        checked = st.checkbox(doc_name, key=f"doc_checkbox_{i}")

        if checked:
            selected_docs.append(doc_name)

    if st.button("Delete Selected Documents", key="delete_docs_btn"):

        if not selected_docs:

            st.warning("Select documents first")

        else:

            with st.spinner("Deleting documents..."):

                try:

                    res = requests.post(
                        f"{API_URL}/api/documents/delete",
                        json={"documents": selected_docs}
                    )

                    if res.status_code == 200:

                        st.success(f"{len(selected_docs)} document(s) deleted")

                        st.rerun()

                    else:

                        st.error("Delete failed")
                        st.write(res.text)

                except Exception as e:

                    st.error("Backend error")
                    st.write(e)


# ----------------------------------------------------
# CHAT PANEL
# ----------------------------------------------------

with col2:

    st.header("💬 Ask Questions")

    question = st.text_input(
        "Ask a question",
        key="chat_question"
    )

    selected_document = st.selectbox(
        "Optional: Select specific document",
        ["None"] + [doc if isinstance(doc, str) else doc.get("name") for doc in documents],
        key="doc_selector"
    )

    if st.button("Ask", key="ask_btn"):

        if not question:

            st.warning("Enter a question first")

        else:

            payload = {
                "message": question
            }

            if selected_document != "None":
                payload["document"] = selected_document

            with st.spinner("Thinking..."):

                try:

                    res = requests.post(
                        f"{API_URL}/api/chat",
                        json=payload
                    )

                    if res.status_code == 200:

                        data = res.json()

                        st.subheader("Answer")

                        st.write(data.get("response", "No response"))

                        sources = data.get("sources", [])

                        if sources:

                            st.subheader("Sources")

                            for s in sources:

                                st.markdown(
                                    f"""
                                    **Document:** {s.get("source")}

                                    **Score:** {round(s.get("score", 0), 3)}

                                    ```
                                    {s.get("content")}
                                    ```
                                    """
                                )

                    else:

                        st.error("Chat request failed")
                        st.write(res.text)

                except Exception as e:

                    st.error("Backend connection failed")
                    st.write(e)

# ----------------------------------------------------
# STATISTICS PANEL
# ----------------------------------------------------

with col3:

    st.header("📊 AI Statistics")

    try:

        res = requests.get(f"{API_URL}/api/documents/stats")

        if res.status_code == 200:

            stats = res.json().get("statistics", {})

            st.metric("Documents", stats.get("total_documents", 0))
            st.metric("Chunks", stats.get("total_chunks", 0))
            st.metric("Tokens Indexed", stats.get("total_tokens", 0))

        else:
            st.warning("Statistics unavailable")

    except:
        st.warning("Backend not reachable")