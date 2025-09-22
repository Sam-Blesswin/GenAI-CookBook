# 🚀 Prompt Engineering with LangChain

The goal is simple: **learn how to communicate with Large Language Models (LLMs) effectively** by understanding different styles of prompts.

---

## 🌟 What is Prompt Engineering?

Prompt Engineering is the practice of **designing instructions** (prompts) that guide a language model to produce the desired output.
The same model can behave very differently depending on how you phrase your instructions.

Think of prompts as the **user manual for the model** — the better you write them, the better the model performs.

---

## 📖 Prompting Techniques Covered

This project covers five essential techniques:

---

### 1️⃣ Zero-Shot Prompting

* **Definition**: The model is asked to perform a task **without seeing any examples**.
* **Usage**: Best when the task is simple, clear, and the model already has enough background knowledge.
* **Example Task**: *Translate this sentence into French.*

👉 Teaches the model to rely purely on its **pre-trained knowledge**.

---

### 2️⃣ One-Shot Prompting

* **Definition**: The model is given **a single example** before being asked to solve a new case.
* **Usage**: Useful when you want to show the model the **format or style** of the expected output.
* **Example Task**: Provide one review and its sentiment, then ask the model to classify a new review.

👉 Helps the model **learn the pattern** from one demonstration.

---

### 3️⃣ Few-Shot Prompting

* **Definition**: The model is provided with **multiple examples (2–5)** before being asked to solve a new problem.
* **Usage**: Effective when tasks are complex or nuanced, where **one example is not enough**.
* **Example Task**: Provide several word–antonym pairs, then ask the model to find the antonym of a new word.

👉 Gives the model a **stronger context** and improves reliability.

---

### 4️⃣ Chain-of-Thought (CoT) Prompting

* **Definition**: The model is encouraged to **reason step by step** before giving the final answer.
* **Usage**: Best for math problems, logical reasoning, or multi-step decision making.
* **Example Task**: Ask the model to calculate profit percentage by explicitly telling it to "think step by step."

👉 Improves **reasoning accuracy** by making the model **show its work**.

---

### 5️⃣ Self-Consistency Prompting

* **Definition**: The model generates **multiple independent solutions**, then compares them to select the most consistent result.
* **Usage**: Especially powerful for tricky reasoning tasks where the model might make small errors in one attempt.
* **Example Task**: Solve the “sister’s age” riddle in three different ways and determine the consistent answer.

👉 Boosts **robustness** by combining multiple reasoning paths into one reliable answer.

---

## 🎯 Why These Techniques Matter

* **Zero-Shot** → Quick tasks, no examples needed.
* **One-Shot** → Show format/style.
* **Few-Shot** → Teach patterns through examples.
* **Chain-of-Thought** → Better reasoning and fewer mistakes.
* **Self-Consistency** → Higher reliability through multiple solutions.
