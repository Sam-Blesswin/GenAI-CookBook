import os
from datetime import datetime
import requests
import pytz
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from pydantic import BaseModel, Field

load_dotenv()

class WeatherInput(BaseModel):
    """Input schema for weather tool"""
    location: str = Field(description="The city and state/country, e.g. 'New York, NY' or 'London, UK'")

class TimeInput(BaseModel):
    """Input schema for time tool"""
    timezone: str = Field(default="local", description="The timezone (optional, defaults to local time). Examples: 'UTC', 'US/Eastern', 'Europe/London', 'Asia/Tokyo', or 'local' for system timezone")

@tool("get_weather", args_schema=WeatherInput)
def get_weather(location: str) -> str:
    """Get current weather information for a city."""    
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return "Weather API key not configured. Please set WEATHER_API_KEY environment variable."
        
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "imperial"
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            return f"Weather in {location}: {temp}°C, {description}, humidity: {humidity}%"
        else:
            return f"Could not get weather for {location}. Error: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"



@tool("get_current_time", args_schema=TimeInput)
def get_current_time(timezone: str = "local") -> str:
    """Get the current time and date in the specified timezone"""
    try:
        if timezone.lower() == "local":
            # Use local system timezone
            current_time = datetime.now()
            tz_name = "Local System Time"
        else:
            # Convert to specified timezone
            try:
                tz = pytz.timezone(timezone)
                current_time = datetime.now(tz)
                tz_name = timezone
            except pytz.UnknownTimeZoneError:
                timezone_map = {
                    'EST': 'US/Eastern',
                    'PST': 'US/Pacific',
                    'CST': 'US/Central',
                    'MST': 'US/Mountain',
                    'GMT': 'GMT',
                    'BST': 'Europe/London',
                    'CET': 'Europe/Paris',
                    'JST': 'Asia/Tokyo'
                }
                
                if timezone.upper() in timezone_map:
                    tz = pytz.timezone(timezone_map[timezone.upper()])
                    current_time = datetime.now(tz)
                    tz_name = timezone_map[timezone.upper()]
                else:
                    return f"Unknown timezone: {timezone}. Please use standard timezone names like 'UTC', 'US/Eastern', 'Europe/London', etc."
        
        time_info = f"""Current Time Information:
Date: {current_time.strftime('%Y-%m-%d')}
Time: {current_time.strftime('%H:%M:%S')}
Timezone: {tz_name}
Day: {current_time.strftime('%A')}
UTC Offset: {current_time.strftime('%z') if hasattr(current_time, 'tzinfo') and current_time.tzinfo else 'N/A'}"""
        
        return time_info
    except Exception as e:
        return f"Error getting current time: {str(e)}"



def run_simple_react_agent():
    """
    Run the simple ReAct agent in an interactive loop.
    """
    print("🤖 LangGraph Simple ReAct Agent (using create_react_agent)")
    print("=" * 60)
    print("This agent demonstrates the streamlined create_react_agent method.")
    print("It can help you with:")
    print("• Weather information (e.g., 'What's the weather in London?')")
    print("• Current time (e.g., 'What time is it?')")
    print("• Type 'quit' to exit")
    print("=" * 60)
    
    # Create the agent
    """
    Create a ReAct agent using LangGraph's create_react_agent method.
    
    This is much simpler than manually building the StateGraph but offers
    less customization compared to the manual approach.
    """
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Define our tools
    tools = [get_weather, get_current_time]
    
    # Create a custom prompt for the ReAct agent
    prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful ReAct agent with access to several tools.

Available tools:
- get_weather: Get weather information for any city
- get_current_time: Get the current date and time

When solving problems:
1. Think step by step (Reasoning)
2. Use appropriate tools when needed (Acting)
3. Provide clear, helpful responses
4. Always explain your reasoning before taking actions

If you need to use a tool, call it and then provide a response based on the results."""),
    MessagesPlaceholder(variable_name="messages"),
])
    
    # Create the ReAct agent using the built-in method
    # This automatically handles:
    # - State management
    # - Tool routing
    # - Message handling
    # - Graph constructionclear
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt,
        checkpointer=MemorySaver(),
        debug=True,
    )
    
    # Configuration for the agent (enables memory)
    config = {"configurable": {"thread_id": "simple-react-agent-session"}}
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\n🤔 Agent is thinking...")
            
            # Invoke the agent with the user's message
            response = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=config
            )
            
            # Get the last message from the agent
            last_message = response["messages"][-1]
            
            if hasattr(last_message, 'content'):
                print(f"\n🤖 Agent: {last_message.content}")
            else:
                print(f"\n🤖 Agent: {last_message}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again.")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        exit(1)
    
    run_simple_react_agent()
