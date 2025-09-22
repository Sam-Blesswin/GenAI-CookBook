import os
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.tools import tool
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
    """Get current weather information for a specific location"""
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
        
        # Extract relevant weather information
        weather_info = {
            "location": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        
        result = f"""Weather in {weather_info['location']}, {weather_info['country']}:
Temperature: {weather_info['temperature']:.1f}°F (feels like {weather_info['feels_like']:.1f}°F)
Conditions: {weather_info['description'].title()}
Humidity: {weather_info['humidity']}%
Wind Speed: {weather_info['wind_speed']} mph \n"""
        
        return result
        
    except Exception as e:
        return f"Error getting weather: {str(e)}"

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

class ToolCallingAgent:    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            model="gpt-4o",
            openai_api_key=openai_api_key,
            temperature=0.0,
        )
        
        # Initialize tools
        self.tools = [get_weather, get_current_time]
        

        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant with access to external tools for real-time information.

IMPORTANT: You MUST use the available tools when users ask for real-time information. Do not provide generic responses.

When a user asks about:
- Time/current time/what time is it -> ALWAYS use get_current_time tool
- Weather/temperature/conditions -> ALWAYS use get_weather tool

Available tools:
- get_weather: Get current weather for any location
- get_current_time: Get current time and date

You must call the appropriate tools to get real-time data before responding."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create the agent
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
    
    def process_query(self, user_query: str) -> str:
        """Process a user query through the complete tool calling workflow"""
        print(f"\n🤖 Processing query: '{user_query}'")
        print("=" * 60)
        
        try:
            print("📝 Step 1: LLM analyzing query and determining tool needs...")
            print(f"🔧 Available tools: {[tool.name for tool in self.tools]}")
            
            response = self.agent_executor.invoke({
                "input": user_query
            })
            
            final_answer = response.get("output", "I apologize, but I couldn't process your request.")
            
            print("✅ Task completed!")
            return final_answer
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            print(f"❌ Error: {error_msg}")
            return error_msg
    
def main():
    """Main interactive loop"""
    print("🚀 LangChain Tool Calling Agent - AI Assistant with Real-time Tools")
    print("🔗 Powered by LangChain + OPENAI API")
    print("=" * 70)
    
    openai_key = os.getenv("OPENAI_API_KEY")
    weather_key = os.getenv("WEATHER_API_KEY")
    
    if not openai_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please add your OpenAI API key to a .env file")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        return
    
    if not weather_key:
        print("⚠️  Warning: WEATHER_API_KEY not found. Weather functionality will be limited.")
        print("Get a free API key from: https://openweathermap.org/api")
    
    try:
        agent = ToolCallingAgent(openai_key)
        print("✅ Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {str(e)}")
        return
    
    print("\n🎯 Example queries to try:")
    print("- 'What is the weather in New York?'")
    print("- 'What time is it?'")
    print("- 'Tell me about the weather in London and what time it is'")
    
    while True:
        try:
            user_input = input("🗣️  You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
                
            response = agent.process_query(user_input)
            print(f"\n🤖 Assistant: {response}\n")
            print("-" * 70)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()