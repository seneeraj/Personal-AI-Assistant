# Personal AI Assistant (RAG-based)

An AI-powered document assistant that allows users to upload PDF documents and ask questions about them.
The system uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant document content and generate contextual answers.

The assistant works locally using **FastAPI, Streamlit, Sentence Transformers, and ChromaDB**.

---

# Features

* Upload PDF documents
* Semantic search using vector embeddings
* Ask natural language questions
* Answers generated using LLM + document context
* Source document references
* Document statistics dashboard
* Multi-document retrieval with document ranking

---

# System Architecture

User Question
↓
Query Expansion
↓
Vector Search (ChromaDB)
↓
Document Ranking
↓
Context Retrieval
↓
LLM Response Generation
↓
Answer + Source Document

---

# Project Structure

```
Personal_AI_Assistant
│
├── backend
│   ├── agents
│   ├── api
│   ├── orchestrator
│   ├── rag
│   ├── services
│   └── main.py
│
├── frontend
│   └── app.py
│
├── documents
│   └── .gitkeep
│
├── requirements.txt
├── app.bat
├── LICENSE
├── README.md
└── .gitignore
```

---

# Requirements

Before running the project ensure the following are installed:

* Python 3.10+
* pip
* Internet connection (for installing dependencies)

---

# Installation

Clone the repository:

```
git clone https://github.com/your-username/personal-ai-assistant.git
cd personal-ai-assistant
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Running the Project

There are **two ways** to run the project.

---

## Method 1 (Recommended)

Double click the file:

```
app.bat
```

This will automatically start:

* Backend (FastAPI server)
* Frontend (Streamlit interface)

Open your browser and go to:

```
http://localhost:8501
```

---

## Method 2 (Manual Start)

### Start Backend

```
uvicorn backend.main:app --host 0.0.0.0 --port 8010
```

### Start Frontend

Open another terminal:

```
streamlit run frontend/app.py
```

Then open:

```
http://localhost:8501
```

---

# How to Use the Application

1. Upload a PDF document
2. Wait for the document to be processed
3. Enter a question in the chat interface
4. The system retrieves relevant document content
5. The assistant generates an answer with source references

---

# Example Questions

* What is Startup India?
* When is the capstone project?
* Summarize the uploaded document
* What are the key points in this report?

---

# Technologies Used

* Python
* FastAPI
* Streamlit
* Sentence Transformers
* ChromaDB
* PDFPlumber
* NumPy

---

# Future Improvements

* Hybrid search (vector + keyword)
* Cross-encoder reranking
* Multi-document reasoning
* Cloud deployment
* Conversation memory
* Support for DOCX and TXT files

---

# License

This project is licensed under the MIT License.

See the **LICENSE** file for details.

---

# Author

Neeraj Bhatia
