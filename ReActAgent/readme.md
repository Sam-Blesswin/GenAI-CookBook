# LangGraph ReAct Agent

A simple ReAct (Reasoning + Acting) agent implementation using LangGraph's `create_react_agent` method.

## 🎯 What is a ReAct Agent?

ReAct (Reasoning + Acting) is a paradigm that combines:
- **Reasoning**: The agent thinks through problems step by step
- **Acting**: The agent uses tools to gather information or perform actions

This creates a more reliable and transparent AI agent that can explain its thought process.

## 🛠️ Features of This Implementation

### **Tools Available:**
1. **Weather Tool**: Get current weather information for any city using OpenWeatherMap API
2. **Time Tool**: Get current date and time in any timezone (supports local time and international timezones)

### **LangGraph Features Demonstrated:**
- `create_react_agent`: Simplified ReAct agent creation
- Built-in tool execution and routing
- `MemorySaver`: Conversation persistence across sessions
- Automatic state management
- Streamlined prompt integration

## 🏃‍♂️ Usage

The agent demonstrates the streamlined create_react_agent method and can help you with:
• Weather information (e.g., 'What's the weather in Lehi, Utah?')
• Current time in any timezone (e.g., 'What's the time there?')
• Type 'quit' to exit

### Example Interactions:

```
💬 You: What's the weather in Lehi, Utah?
🤖 Agent: I'll check the current weather in Lehi, Utah for you.
[Agent uses weather tool]
Weather in Lehi, Utah: 68°F, clear sky, humidity: 45%

💬 You: What's the time there?
🤖 Agent: Let me get the current time in Utah for you.
[Agent uses time tool]
Current Time Information:
Date: 2025-09-25
Time: 14:04:08
Timezone: US/Mountain
Day: Wednesday
UTC Offset: -0600
```

What's the time there? - 'there' refers to the location in the previous chat here. Its possible due to the memory persistence.

### **Key Components:**

1. **Tools**: `@tool` decorated functions with Pydantic schemas for input validation
2. **LLM Integration**: ChatOpenAI with GPT-4o-mini model
3. **Agent Creation**: `create_react_agent` for simplified setup
4. **Memory**: MemorySaver for conversation persistence
5. **Interactive Loop**: Terminal-based conversation interface with error handling
