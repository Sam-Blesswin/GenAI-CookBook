# LCEL Chaining Demo (LangChain + Gemini)

This project shows how to build and run **LangChain Expression Language (LCEL)** chains with Google’s Gemini LLM.

We explore two main styles of chaining:

---

## 🚀 Sequence Chain

* **Use when:** You need a **pipeline**, where each step feeds into the next.
* **Example:** Prompt → LLM → Post-process.
* **Pros:**

  * Single LLM call (fast & cheap)
  * Simpler code
* **Cons:**

  * Harder to reuse pieces individually
  * If one part fails, you rerun the whole pipeline

---

## ⚡ Parallel Chain

* **Use when:** You want to **fan out** the same input into multiple independent outputs.
* **Example:** From one review, run **sentiment analysis**, **feature extraction**, and **summary** in parallel.
* **Pros:**

  * Modular, reusable tasks
  * Different prompts/models per task
  * Outputs come back structured in a dict
* **Cons:**

  * Multiple LLM calls (slower, more \$\$)

---

## 📂 Files

* `sequence_chain.py` → One-shot pipeline (sequence)
* `parallel_chain.py` → Multiple sub-tasks in parallel
* `main.py` → Runs either sequence or parallel chain based on a toggle

---

## 🔑 Key Idea

* **Sequence = assembly line** (linear, dependent steps).
* **Parallel = fork** (independent, simultaneous branches).
