# Import the agent executor from model_manager
from model_manager import agent_executor

# Import HumanMessage and AIMessage from langchain.schema
from langchain.schema import HumanMessage, AIMessage
from colorama import Fore, Style

# Initialize an empty list to store the chat history
chat_history = []
# Initialize an empty list to store the last conversation
last_conversation = []
# Start an infinite loop to continuously take user input
while True:
    # Get user input
    prompt = input(f"{Fore.GREEN}User: {Style.RESET_ALL}")
    # If the input contains "//" break the loop
    if "//" in prompt:
        break
    try:
        # Invoke the agent executor with the chat history, input, and last conversation
        result = agent_executor.invoke(
            {
                "chat_history": chat_history,
                "input": prompt,
                "last_conversation": last_conversation,
            }
        )
        # Print the agent's thoughts and actions
        if "intermediate_steps" in result:
            for step in result["intermediate_steps"]:
                if isinstance(step, tuple) and len(step) >= 2:
                    action = step[0]
                    observation = step[1]
                    print(action.log)

        # Get the output from the agent executor
        answer = result["output"]
        # Update the last conversation with the user input and the agent's answer
        last_conversation = [HumanMessage(content=prompt), AIMessage(content=answer)]
        # Extend the chat history with the last conversation
        chat_history.extend(last_conversation)
        # If the chat history is longer than 5, keep only the last 5 entries
        if len(chat_history) > 5:
            chat_history = chat_history[-5:]
        # Print the agent's answer
        print(f"{Fore.GREEN}Assistant: {Fore.CYAN}{answer.strip()}{Style.RESET_ALL}")
        print("_________________________")
    # Catch any exceptions that occur during the process
    except Exception as e:
        # Print the error message
        print(f"\nError: {str(e)}")
        # Print a message asking the user to rephrase their question
        print("Try rephrasing your question or providing more context.")
