# Import the agent executor from model_manager
from model_manager import agent_executor
# Import HumanMessage and AIMessage from langchain.schema
from langchain.schema import HumanMessage, AIMessage

# Initialize an empty list to store the chat history
chat_history = []
# Initialize an empty list to store the last conversation
last_conversation = []
# Start an infinite loop to continuously take user input
while True:
    # Get user input
    prompt = input("User: ")
    # If the input contains "//" break the loop
    if "//" in prompt:
        break
    try:
        # Invoke the agent executor with the chat history, input, and last conversation
        result = agent_executor.invoke({
            "chat_history": chat_history,
            "input": prompt,
            "last_conversation": last_conversation
        })
        # Get the output from the agent executor
        answer = result["output"]
        # Update the last conversation with the user input and the agent's answer
        last_conversation = [
            HumanMessage(content=prompt),
            AIMessage(content=answer)
            ]
        # Extend the chat history with the last conversation
        chat_history.extend(last_conversation)
        # If the chat history is longer than 5, keep only the last 5 entries
        if len(chat_history) > 5:
            chat_history[-5:]
        # Print the agent's answer
        print("\nAssistant:", answer.strip())
    # Catch any exceptions that occur during the process
    except Exception as e:
        # Print the error message
        print(f"\nError: {str(e)}")
        # Print a message asking the user to rephrase their question
        print("Try rephrasing your question or providing more context.")