# AI-Powered Document Intelligence Assistant using RAG

## Project Overview

The AI-Powered Document Intelligence Assistant is a local AI application that allows users to upload PDF documents and ask questions about their content.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate context-based answers using a locally running Large Language Model (LLM).

## Key Features

- **PDF Processing:** Extracts text and page information from PDF documents.
- **Text Chunking:** Splits extracted text into smaller chunks for efficient retrieval.
- **Embeddings:** Converts text chunks into numerical vectors using Sentence Transformers.
- **Vector Search:** Uses FAISS to retrieve relevant document chunks.
- **Question Answering:** Generates answers using the retrieved context and a local LLM.
- **Document Summarization:** Supports basic summarization through agent-style tool routing.
- **Input Guardrails:** Checks user inputs for empty questions, excessive length, and selected suspicious phrases.
- **RAG Evaluation:** Measures keyword-based retrieval coverage, answer keyword coverage, and response time.

## Technologies Used

- Python
- Streamlit
- PyMuPDF
- Sentence Transformers
- FAISS
- Ollama
- Qwen2.5:3B
- NumPy
- Pandas

## Project Architecture

1. User uploads a PDF document through the Streamlit interface.
2. PyMuPDF extracts text from the PDF.
3. The text is divided into smaller chunks.
4. Sentence Transformers generates embeddings for the chunks.
5. FAISS stores and searches the embeddings.
6. The user's question is converted into an embedding and relevant chunks are retrieved.
7. The retrieved context and question are passed to the local Qwen2.5:3B model through Ollama.
8. The model generates an answer based on the retrieved document context.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Document-Assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and start Ollama

Install Ollama on your computer, then download the model:

```bash
ollama pull qwen2.5:3b
```

Make sure the Ollama service is running.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Evaluation Results

Initial evaluation results from the project:

| Metric | Result |
|---|---:|
| Average Retrieval Keyword Score | 100% |
| Average Answer Keyword Score | 66.67% |
| Average Response Time | 14.12 seconds |

**Note:** These are basic keyword-based evaluation metrics, not comprehensive measures of answer correctness or faithfulness.

## Limitations

- The application currently maintains one active document index at a time.
- Input guardrails use basic rule-based checks and cannot detect every prompt injection attempt.
- Evaluation uses keyword-based metrics rather than advanced RAG evaluation frameworks.
- Response time depends on local hardware and model performance.

## Future Improvements

- Support multiple documents and persistent document collections.
- Improve prompt-injection protection and output validation.
- Add advanced RAG evaluation using faithfulness and retrieval-quality metrics.
- Implement semantic routing and more advanced agent workflows.
- Add AWS Bedrock integration as a future cloud-based option.

## Author

Developed as a hands-on Generative AI and RAG project using locally running models.
