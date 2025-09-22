# 🛠️ LangChain Tool Calling Agent

This project demonstrates how to build a **tool-using AI assistant** with [LangChain](https://www.langchain.com/).
The assistant uses **OpenAI's GPT models** and integrates with external tools for **real-time data** like **weather** and **time**.

---

## 🚀 Features

* **LangChain Agent**: Built with `create_tool_calling_agent` and `AgentExecutor`
* **Tool Calling**: The LLM decides when to call tools
* **Weather Tool**: Fetches live weather data from OpenWeatherMap API
* **Time Tool**: Gets the current time in any timezone

---

## ⚙️ How It Works

1. **User Query**: You ask something like *“What’s the weather in London?”*
2. **LLM Decision**: The model analyzes your request and decides which tool to use.
3. **Tool Execution**: The agent runs the tool (`get_weather` or `get_current_time`).
4. **Result Integration**: Tool results are passed back to the model.
5. **Final Response**: The assistant replies with natural, real-world data.

---

## 📋 Requirements

* API Keys:

  * `OPENAI_API_KEY` (from [OpenAI](https://platform.openai.com/))
  * `WEATHER_API_KEY` (from [OpenWeatherMap](https://openweathermap.org/api)) – optional, but needed for weather queries

---

### Example Interactions

```
🗣️  You: What is the weather in New York?

🤖 Assistant:
Weather in New York, US:
Temperature: 68.5°F (feels like 70.2°F)
Conditions: Clear Sky
Humidity: 45%
Wind Speed: 8.2 mph
```

```
🗣️  You: What time is it in Tokyo?

🤖 Assistant:
Current Time Information:
Date: 2025-09-22
Time: 23:42:15
Timezone: Asia/Tokyo
Day: Monday
UTC Offset: +0900
```

---

## 🔧 Tools

* **`get_weather`**
  Input: City name (e.g., `"London, UK"`)
  Output: Temperature, weather conditions, humidity, wind

* **`get_current_time`**
  Input: Timezone (e.g., `"UTC"`, `"US/Eastern"`, or `"local"`)
  Output: Current date, time, day of week, UTC offset

---

## 📚 Key Components

* **`create_tool_calling_agent`**: Builds the LangChain agent with tool-calling abilities
* **`AgentExecutor`**: Executes the full workflow (LLM → tool → result → response)
* **`ChatPromptTemplate`**: Ensures the LLM knows when to use tools
* **Pydantic Models**: Define structured input for tools



