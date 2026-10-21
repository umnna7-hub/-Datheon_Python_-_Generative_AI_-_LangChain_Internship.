
from pathlib import Path
import logging, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger("pypdf").setLevel(logging.ERROR)
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


PROJECT_DIR = Path(__file__).parent
PDF_PATHS = [
    PROJECT_DIR / "documents" / "AIinComputerScience.pdf",
    PROJECT_DIR / "documents" / "AI.pdf",
    PROJECT_DIR / "documents" / "Introduction.pdf",
]


def load_pdf(pdf_path: Path):
    """Load a PDF and preserve its page metadata."""
    loader = PyPDFLoader(str(pdf_path))
    pages = loader.load()

    if not pages:
        raise ValueError("The PDF contains no extractable pages.")

    return pages


def split_documents(pages):
    """Split PDF pages into smaller text chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    return splitter.split_documents(pages)


def create_vector_store(chunks):
    """Store document chunks and embeddings in ChromaDB."""
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text:latest"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(PROJECT_DIR / "chroma_db"),
        collection_name="pdf_documents",
    )

    return vector_store


def search_documents(vector_store, question):
    """Find the most relevant PDF chunks."""
    results = vector_store.similarity_search(
        question,
        k=3,
    )

    unique_results = []
    seen_text = set()

    for result in results:
        text = result.page_content.strip()

        if text not in seen_text:
            seen_text.add(text)
            unique_results.append(result)

    return unique_results

def generate_answer(question, results):
    """Answer using only the retrieved PDF passages."""

    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0,
    )

    context_parts = []

    for result in results:
        page_number = result.metadata.get("page", 0) + 1
        source = result.metadata.get("source", "Unknown PDF")

        context_parts.append(
            f"Source PDF: {source}, Page {page_number}:\n"
            f"{result.page_content}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a PDF question-answering assistant.

Answer using ONLY the context below.
If the answer is not present, say:
"I could not find that information in the provided documents."

Do not use outside knowledge.
Cite the PDF filename and page number for factual answers.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content


def main():
    try:
        all_pages = []

        for pdf_path in PDF_PATHS:
            if not pdf_path.exists():
                print(f"PDF not found: {pdf_path}")
                continue

            pages = load_pdf(pdf_path)

            # Keep track of which PDF each page came from
            for page in pages:
                page.metadata["source"] = pdf_path.name

            all_pages.extend(pages)
            print(f"Loaded {pdf_path.name}: {len(pages)} pages")

        if not all_pages:
            print("No PDFs were loaded. Check your file paths.")
            return

        chunks = split_documents(all_pages)
        vector_store = create_vector_store(chunks)

        print(f"\nTotal pages loaded: {len(all_pages)}")
        print(f"Total text chunks: {len(chunks)}")
        print("ChromaDB database created successfully!")

        question = input("\nAsk a question about your PDFs: ")
        results = search_documents(vector_store, question)
        answer = generate_answer(question, results)

        print("\nAI Answer:")
        print(answer)

        print("\nRetrieved information:")
        for result in results:
            page_number = result.metadata.get("page", 0) + 1
            source = result.metadata.get("source", "Unknown PDF")

            print(f"\nSource PDF: {source} | Page: {page_number}")
            print(result.page_content[:300])
            print("-" * 40)

    except Exception as error:
        print(f"Could not process the PDFs: {error}")


if __name__ == "__main__":
    main()