# RAG Application

A simple terminal-based Retrieval-Augmented Generation (RAG) application that allows you to load PDF documents, store them in ChromaDB, and ask questions about their content using LangChain and OpenAI.

## 📌 What is RAG?

**Retrieval-Augmented Generation (RAG)** is an AI pattern that combines:

* **Retrieval** → Searching for the most relevant information from a knowledge base (e.g., stored documents).
* **Generation** → Using a Large Language Model (LLM) to generate answers based on both the retrieved data and the query.

This allows LLMs to give more **accurate, up-to-date, and source-cited answers**, without needing all the knowledge baked directly into the model.

## Features

- 📄 Load PDF documents from file paths
- 🗄️ Store document embeddings in ChromaDB (persistent storage)
- ❓ Ask questions about loaded documents
- 🔍 Get answers with source citations
- 💾 Persistent storage - documents remain available between sessions

## Usage

The application provides a simple menu interface:

1. **Load a PDF file** - Enter the path to your PDF file to load and process it
2. **Ask a question** - Query the loaded documents
3. **Show vectorstore info** - See how many document chunks are stored
4. **Exit** - Close the application

## How it Works

1. **Document Loading**: PDFs are loaded using LangChain's PyPDFLoader
2. **Text Splitting**: Documents are split into chunks for better retrieval
3. **Embeddings**: Text chunks are converted to embeddings using OpenAI's embedding model
4. **Vector Storage**: Embeddings are stored in ChromaDB for fast similarity search
5. **Question Answering**: Questions are answered using a RetrievalQA chain that:
   - Finds relevant document chunks using similarity search
   - Uses OpenAI to generate answers based on retrieved context
   - Provides source citations

## Data Persistence

- ChromaDB data is stored in the `./chroma_db` directory
- Documents remain available between application sessions
- You can add multiple PDFs to build a larger knowledge base


## ⚙️ LangChain Components Used

### 🔹 RecursiveCharacterTextSplitter

Splits long documents into smaller, overlapping chunks to make them manageable for embeddings and LLM context limits.

* **`chunk_size=1000`** → Max characters (or tokens if customized) in each chunk.
* **`chunk_overlap=200`** → Number of characters repeated between consecutive chunks.

✅ **Why chunk overlap?**
Overlap ensures **context continuity** across chunks. Without it, important sentences that cross a chunk boundary could get lost. Overlapping preserves meaning when chunks are later retrieved.

### 🔹 RetrievalQA

A LangChain chain designed for **Question Answering over documents**.

What it does:

1. Embeds the query into a vector.
2. Retrieves the **top-k most similar chunks** from the vector store.
3. Passes those chunks + query to an LLM to generate an answer.
4. (Optional) Returns source documents for citations.

**Chain Types:**

* **`stuff`** → Simple: “stuff” all retrieved docs into one prompt. Fast but limited by LLM context.
* **`map_reduce`** → Process chunks individually (“map”), then combine results (“reduce”). Good for large sets.
* **`refine`** → Iteratively improves the answer by feeding chunks one by one.
* **`map_rerank`** → Scores answers from each chunk, then selects the best one.

## 🗄️ Storing Embeddings in a Vector DB

When you add documents, each chunk goes through three steps:

1. **Vector** → The numeric embedding of the text, created using an embedding model.
2. **Original Data** → The actual chunk text.
3. **Metadata** → Info about the chunk (e.g., document name, page number).

These are stored in **ChromaDB**, which provides **similarity search** capabilities.

### 🔍 Indexing Algorithm

Chroma uses structures like **HNSW (Hierarchical Navigable Small World graphs)** for efficient **Approximate Nearest Neighbor (ANN) search**.

* Instead of comparing a query vector to every stored embedding, HNSW speeds up retrieval by navigating a graph of vectors.
* This makes retrieval fast, even with thousands or millions of embeddings.

---

written by ChatGPT