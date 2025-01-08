# Importing necessary libraries from langchain and other packages
from langchain import hub
from langchain_google_genai import GoogleGenerativeAI
# Importing custom tools and prompts
from tools import tools
from prompts import agent_prompt
# Importing agent creation and execution modules
from langchain.agents import AgentExecutor, create_react_agent
import os
# Importing dotenv for environment variables
from dotenv import load_dotenv
load_dotenv()

llm = GoogleGenerativeAI(
    google_api_key=os.getenv("GOOGLE_GEMINI_API2"),
    model="gemini-2.0-flash-exp"
)

# Load the react prompt from langchain hub and set custom template
react_docstore_prompt = hub.pull("hwchase17/react-chat")
react_docstore_prompt.template = agent_prompt

# Create the react agent with gemini model, tools and prompt
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_docstore_prompt,

)
# Create the agent executor with the agent and tools, enable error handling and verbose mode
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)
