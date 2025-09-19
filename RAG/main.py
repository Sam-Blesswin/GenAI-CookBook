import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

load_dotenv()


class RAGApplication:
    def __init__(self, persist_directory="./chroma_db"):
        """Initialize the RAG application with ChromaDB storage."""
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.llm = ChatOpenAI(
            model="gpt-4o", openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vectorstore = None
        self.qa_chain = None

        # Create persist directory if it doesn't exist
        Path(persist_directory).mkdir(parents=True, exist_ok=True)

        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Initialize or load existing ChromaDB vectorstore."""
        try:
            # Try to load existing vectorstore
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
            )
            print(f"✅ Loaded existing ChromaDB from {self.persist_directory}")
        except Exception as e:
            print(
                f"⚠️  No existing ChromaDB found. Will create new one when documents are added."
            )
            self.vectorstore = None

    def load_pdf(self, pdf_path):
        """Load and process a PDF file."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if not pdf_path.lower().endswith(".pdf"):
            raise ValueError("File must be a PDF")

        print(f"📄 Loading PDF: {pdf_path}")

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        texts = text_splitter.split_documents(documents)
        print(f"📝 Split PDF into {len(texts)} chunks")

        return texts

    def add_documents_to_vectorstore(self, documents):
        """Add documents to ChromaDB vectorstore."""
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
            )
            print("🆕 Created new ChromaDB vectorstore")
        else:
            # Add to existing vectorstore
            self.vectorstore.add_documents(documents)
            print("➕ Added documents to existing ChromaDB vectorstore")

        self._initialize_qa_chain()

    def _initialize_qa_chain(self):
        """Initialize the QA chain with the vectorstore."""
        if self.vectorstore is None:
            raise ValueError("Vectorstore not initialized. Please add documents first.")

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
        )
        print("🔗 QA chain initialized")

    def ask_question(self, question):
        """Ask a question and get an answer based on the stored documents."""
        if self.qa_chain is None:
            if self.vectorstore is None:
                raise ValueError("No documents loaded. Please add a PDF first.")
            self._initialize_qa_chain()

        print(f"❓ Question: {question}")
        print("🤔 Thinking...")

        result = self.qa_chain({"query": question})

        answer = result["result"]
        source_docs = result["source_documents"]

        print(f"💡 Answer: {answer}")
        print(f"\n📚 Sources ({len(source_docs)} documents):")
        for i, doc in enumerate(source_docs, 1):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "Unknown")
            print(f"  {i}. {source} (Page {page})")

        return answer, source_docs

    def get_vectorstore_info(self):
        """Get information about the current vectorstore."""
        if self.vectorstore is None:
            return "No vectorstore initialized"

        try:
            collection = self.vectorstore._collection
            count = collection.count()
            return f"ChromaDB contains {count} document chunks"
        except:
            return "Vectorstore exists but unable to get count"


def main():
    """Main function to run the RAG application."""
    print("🚀 Welcome to the RAG Application!")
    print(
        "This application allows you to load PDF documents and ask questions about them."
    )
    print("=" * 60)

    # Check for OPENAI_API_KEY
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        return

    # Initialize RAG application
    try:
        rag_app = RAGApplication()
        print(f"📊 {rag_app.get_vectorstore_info()}")
    except Exception as e:
        print(f"❌ Error initializing RAG application: {e}")
        return

    while True:
        print("\n" + "=" * 60)
        print("Choose an option:")
        print("1. Load a PDF file")
        print("2. Ask a question")
        print("3. Show vectorstore info")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            pdf_path = input("Enter the path to your PDF file: ").strip()
            try:
                documents = rag_app.load_pdf(pdf_path)
                rag_app.add_documents_to_vectorstore(documents)
                print("✅ PDF successfully loaded and stored in ChromaDB!")
            except Exception as e:
                print(f"❌ Error loading PDF: {e}")

        elif choice == "2":
            if rag_app.vectorstore is None:
                print("⚠️  No documents loaded yet. Please load a PDF first.")
                continue

            question = input("Enter your question: ").strip()
            if question:
                try:
                    rag_app.ask_question(question)
                except Exception as e:
                    print(f"❌ Error answering question: {e}")
            else:
                print("⚠️  Please enter a valid question.")

        elif choice == "3":
            print(f"📊 {rag_app.get_vectorstore_info()}")

        elif choice == "4":
            print("👋 Goodbye!")
            break

        else:
            print("⚠️  Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
