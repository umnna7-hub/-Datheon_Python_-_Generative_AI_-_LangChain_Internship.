# RAG-Based PDF Question Answering System

## 📌 Project Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline that allows users to ask questions about PDF documents and receive answers based on the information retrieved from those documents.

The system combines document loading, text chunking, vector embeddings, semantic search, and a local large language model (LLM).

## ✨ Features

- Load and process multiple PDF documents.
- Extract text while preserving page metadata.
- Split documents into smaller chunks using recursive text splitting.
- Generate embeddings using Ollama's `nomic-embed-text` model.
- Store document embeddings in ChromaDB.
- Retrieve relevant passages using semantic similarity search.
- Generate context-based answers using the `llama3.2:3b` model.
- Display source PDF names and page numbers for retrieved information.

## 🛠️ Technologies Used

- Python
- LangChain
- Ollama
- ChromaDB
- PyPDF
- RecursiveCharacterTextSplitter

## 📂 Project Structure

rag-document-qa/
├── documents/
│   ├── AIinComputerScience.pdf
│   ├── AI.pdf
│   └── Introduction.pdf
├── main.py
├── chroma_db/
└── README.md


## ⚙️ Prerequisites

- Python installed on your computer
- Ollama installed and running
- The following Ollama models:
  - `nomic-embed-text:latest`
  - `llama3.2:3b`

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone (https://github.com/umnna7-hub/-Datheon_Python_-_Generative_AI_-_LangChain_Internship..git)
cd rag-document-qa


### 2. Create and activate a virtual environment

On Windows PowerShell:


python -m venv venv
.\venv\Scripts\Activate.ps1


### 3. Install dependencies


pip install langchain langchain-community langchain-chroma langchain-ollama langchain-text-splitters pypdf


### 4. Download the required Ollama models


ollama pull nomic-embed-text
ollama pull llama3.2:3b


Ensure Ollama is running before executing the application.

### 5. Add your PDF documents

Place your PDF files in the `documents/` directory and update the `PDF_PATHS` list in `main.py` to match their filenames.

### 6. Run the application


python main.py


Enter a question when prompted to receive an answer based on your PDF documents.

## 🔄 How It Works

1. **Document Loading:** Extracts text from multiple PDF files.
2. **Text Chunking:** Splits extracted text into smaller, overlapping chunks.
3. **Embedding Generation:** Converts text chunks into vector representations.
4. **Vector Storage:** Stores embeddings and document metadata in ChromaDB.
5. **Retrieval:** Finds the most relevant chunks for the user's question.
6. **Answer Generation:** Uses a local LLM to generate an answer grounded in the retrieved context.
7. **Source Reference:** Displays the source PDF and page number for retrieved passages.

## 🧪 Current Test Results

- PDF documents loaded: 3
- Total pages loaded: 49
- Text chunks created: 292
- Vector database: ChromaDB
- Embedding model: `nomic-embed-text:latest`
- Language model: `llama3.2:3b`

Example question:

**Question:** How is AI used in computer science?

**Result:** The system retrieved a relevant passage from `AIinComputerScience.pdf`, page 15, discussing mechanisms for monitoring and auditing AI systems for fairness and bias.

## 📌 Limitations

- Answers depend on the content retrieved from the available documents.
- Scanned PDFs may require OCR if their text is not extractable.
- Images and diagrams inside PDFs are not interpreted by the current text-based pipeline.
- Answer quality depends on retrieval relevance and the selected language model.

## 🔮 Future Improvements

- Improve retrieval quality and answer completeness.
- Prevent duplicate chunks when rebuilding the vector database.
- Support more document formats.
- Add a graphical user interface.
- Improve source citations and error handling.

## 👩‍💻 Author

Umna Latif
