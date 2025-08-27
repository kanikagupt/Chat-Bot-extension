import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langchain.schema import SystemMessage
from core.Tools.CursorTools import read_file, read_directory, read_json_file, rename_file, resolve_path, check_file_exists, copy_file, create_and_write_file, create_directory, create_file, write_file, write_json_file, append_file, ask_user, get_file_stats, delete_directory, delete_file, get_systemInfo, run_command

load_dotenv()

class State(TypedDict):
    messages: Annotated[list,add_messages]

tools = [read_file,read_directory,read_json_file,rename_file,resolve_path,check_file_exists,copy_file, create_and_write_file, create_directory, create_file, write_file, write_json_file, append_file, ask_user, get_file_stats, delete_directory, delete_file, get_systemInfo, run_command]

llm = init_chat_model(
    model_provider = "openai", model = "gpt-4o"
)

llm_with_tool = llm.bind_tools(tools = tools)

def chatbot(state: State):
    system_prompt = SystemMessage(content = """
        You are an AI Coding assistance who solve user queries related to code and commands using tools you take input form user 
        and use available suitable tool and run the commands and writes code on the behalf of user. you need just set of instruction from user
        using that you run commands on the user system.if you need user assistance at any point feel free to ask using tool
        
        you can execute command on the behalf of user and solve the user query. but remember don't run any command which can harm the system
        first you need to identify on which system user is working using tool.
        
        Always make sure to keep your generated codes and files in desktop in cursor/ folder. you can create one if not already there on desktop.
        Always make sure what ever you return your final reply to the user make sure it is in the string
        
    """)
    
    message = llm_with_tool.invoke([system_prompt] + state["messages"])
    return {"messages":[message]}

toolnode = ToolNode(tools = tools)
graph_builder = StateGraph(State)

graph_builder.add_node('chatbot',chatbot)
graph_builder.add_node('tools',toolnode)

graph_builder.add_edge(START,'chatbot')
graph_builder.add_conditional_edges('chatbot',tools_condition)
graph_builder.add_edge('tools', 'chatbot')
graph_builder.add_edge('chatbot',END)

# graph = graph_builder.compile()

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

