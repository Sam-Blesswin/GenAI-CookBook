from typing import Annotated

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = init_chat_model("gpt-4o-mini", api_key=api_key)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


try:
    # Generate the graph visualization and save to the same folder as main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    graph_file_path = os.path.join(script_dir, "graph_visualization.png")
    
    graph_png = graph.get_graph().draw_mermaid_png()
    
    with open(graph_file_path, 'wb') as f:
        f.write(graph_png)
    
    print(f"Graph visualization saved to: {graph_file_path}")
    
except Exception as e:
    print(f"Could not generate graph visualization: {e}")
    print("This requires graphviz and other optional dependencies.")

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    stream_graph_updates(user_input)
