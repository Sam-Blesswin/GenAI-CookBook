# GenAI CookBook 🧑‍🍳

A collection of practical examples and implementations for working with Generative AI, focusing on **LangChain, LangGraph, RAG, and MCP Server**.

## 📚 Contents

### [Prompt Engineering](./PromptEngineering/)

Learn effective communication with Large Language Models through various prompting techniques:

* Zero-Shot Prompting
* One-Shot Prompting
* Few-Shot Prompting
* Chain-of-Thought (CoT) Prompting
* Self-Consistency Prompting

### [Chaining](./Chaining/)

Explore LangChain Expression Language (LCEL) patterns:

* **Sequence Chains**: Linear pipelines where each step feeds into the next
* **Parallel Chains**: Fan-out patterns for independent, simultaneous processing

### [RAG](./RAG/)

Build **Retrieval-Augmented Generation (RAG)** applications that combine external knowledge with LLM reasoning:

* **Document Loading** → Extract text from PDFs or other format
* **Embeddings** → Convert chunks into vectors using embedding models
* **Vector Store** → Persist vectors + metadata in **ChromaDB** or other vector databases for similarity search
* **Retrieval** → Query vector store to fetch top-k relevant chunks (using cosine similarity, dot product, etc.)
* **Question Answering** → Use LangChain’s `RetrievalQA` chain

### [ToolCallingAgent](./ToolCallingAgent/)

An interactive example showing how to build a **tool-using AI assistant** with LangChain.  
Demonstrates real-time data retrieval using external tools (e.g., weather, time) via `create_tool_calling_agent` and `AgentExecutor`.

### [ReActAgent](./ReActAgent/)

An interactive example showing how to build a **tool-using AI assistant** with LangGraph.  
Demonstrates real-time data retrieval using external tools (e.g., weather, time) via `create_react_agent`.

---

*This cookbook will continue to grow with new folders and examples as I explore more GenAI concepts and patterns.*

---
