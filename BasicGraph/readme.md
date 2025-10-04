# Chatbot with LangGraph

This project is a **very simple chatbot** built using [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://www.langchain.com/).
It shows how you can connect a Large Language Model (LLM) to a graph workflow and run conversations step-by-step.

---

## ✨ What does this script do?

* Creates a chatbot graph using LangGraph. The graph is very simple:

* START → chatbot → END

* It only has one node: the chatbot itself.

* Connects an LLM (`gpt-4o-mini`) using LangChain’s `init_chat_model`.

* Prints chatbot responses to the console.

* Generates a graph visualization of the flow (`graph_visualization.png`).

---

## 📂 How the script flows

**Define State**

   * `State` is a dictionary that keeps track of messages

**Chatbot Node**

   * The `chatbot` function takes in messages and sends them to the LLM

**Graph Construction**

   * Build a `StateGraph` with:

     * `START → chatbot → END`

**Visualization**

   * Saves a PNG diagram of the graph in the same folder

**Chat Loop**

   * Keeps asking for user input in the terminal
   * Sends the message through the graph
   * Prints the assistant’s reply
   * Ends if you type `quit`, `exit`, or `q`

---

## 📊 Graph Visualization

The script also saves a picture of the chatbot flow:

```
START → chatbot → END
```

The file will be saved as `graph_visualization.png` in the same directory.

---
