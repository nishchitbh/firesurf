# Importing necessary libraries from langchain and other packages
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
# Importing custom tools and prompts
from tools import tools
from prompts import agent_prompt
# Importing agent creation and execution modules
from langchain.agents import AgentExecutor, create_react_agent
import os
from colorama import Fore, Style
# Importing dotenv for environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize the ChatOpenAI model with API key and configurations

models_info = [

    {"model": GoogleGenerativeAI(
        google_api_key=os.getenv("GOOGLE_GEMINI_API"),
        model="gemini-2.0-flash-exp"
    ), "name": "Gemini-2.0-Flash-Exp"},
    {"model": ChatOpenAI(
        api_key=os.getenv("GLHF_API_KEY"),
        base_url="https://glhf.chat/api/openai/v1",
        model="hf:meta-llama/Llama-3.3-70B-Instruct",
    ), "name": "Llama-3.3-70B-Instruct"},

]
models = [model["model"] for model in models_info]
print(f"{Fore.GREEN}Available models: {Style.RESET_ALL}")
for index, model in enumerate(models_info):
    print(f"{index}: {model["name"]}")
model_index = int(input(f"Choose your model {Fore.CYAN}0-{index}:{Style.RESET_ALL} "))

llm = models[model_index]

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
