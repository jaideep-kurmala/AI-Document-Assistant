
import streamlit as st
import os

from src.rag.agent import run_agent
from src.guardrails.input_guardrails import check_input
from src.rag.pdf_processor import extract_pdf
from src.rag.text_chunker import create_chunks
from src.rag.embeddings import create_embeddings
from src.rag.vector_store import save_vectors, search_vectors
from src.rag.rag_chain import generate_answer


# Page settings
st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📚",
    layout="wide"
)

# Application title
st.title("📚 AI Document Intelligence Assistant")

st.write("Upload a PDF and ask questions about its content.")

# Create upload folder
os.makedirs("data/uploads", exist_ok=True)


# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False


# PDF upload
uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


# Process document
if st.button("Process Document"):

    if uploaded_file is None:

        st.warning("Please upload a PDF first.")

    else:

        try:
            with st.spinner("Processing your PDF..."):

                # Save uploaded PDF
                pdf_path = os.path.join(
                    "data/uploads",
                    uploaded_file.name
                )

                with open(pdf_path, "wb") as file:
                    file.write(uploaded_file.getbuffer())

                # Extract PDF text
                pages = extract_pdf(pdf_path)

                # Create chunks
                all_chunks = []

                for page in pages:

                    chunks = create_chunks(page["text"])

                    for chunk in chunks:

                        all_chunks.append({
                            "page": page["page"],
                            "text": chunk
                        })

                if not all_chunks:
                    st.error("No readable text found in this PDF.")

                else:

                    # Generate embeddings
                    vectors = create_embeddings(all_chunks)

                    # Save vectors
                    save_vectors(all_chunks, vectors)

                    st.session_state.document_ready = True
                    st.session_state.messages = []

                    st.success("PDF processed successfully!")

                    st.write("Total pages:", len(pages))
                    st.write("Total chunks:", len(all_chunks))

        except Exception as e:
            st.error(f"Error: {e}")


# Chat section

# Chat section
st.divider()

st.subheader("Chat with your PDF")

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# User question
question = st.chat_input("Ask something about your PDF...")

if question:

    if not st.session_state.document_ready:

        st.warning("Please upload and process a PDF first.")

    else:

        # Check guardrails first
        allowed, message = check_input(question)

        if not allowed:

            st.warning(message)

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": message
            })

        else:

            # Display user question
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):
                st.write(question)

            # Generate answer
            with st.chat_message("assistant"):

                with st.spinner("Finding your answer..."):

                    try:

                        answer = run_agent(question)

                        st.write(answer)

                        # Display sources only for search requests
                        is_summary = (
                            "summarize" in question.lower()
                            or "summary" in question.lower()
                        )

                        if not is_summary:

                            results = search_vectors(question, top_k=3)

                            st.subheader("Sources")

                            for result in results:

                                st.write("Page:", result["page"])

                                st.caption(result["text"][:300])

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })

                    except Exception as e:

                        st.error(f"Error: {e}")
