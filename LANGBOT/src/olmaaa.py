# Importing the required library (ollama)
import ollama

# Initializing an empty list for storing the chat messages and setting up the initial system message
chat_messages = []
system_message = 'You are a helpful assistant.'


# Defining a function to create new messages with specified roles ('user' or 'assistant')
def create_message(message, role):
    return {
        'role': role,
        'content': message
    }


# Starting the main conversation loop
def chat():
    # Calling the ollama API to get the assistant response
    ollama_response = ollama.chat(model='mistral', stream=True, messages=chat_messages)

    # Preparing the assistant message by concatenating all received chunks from the API
    assistant_message = ''

    for chunk in ollama_response:
        assistant_message += chunk['message']['content']

    # Adding the finalized assistant message to the chat log
    chat_messages.append(create_message(assistant_message, 'assistant'))

    # Return the assistant message
    return assistant_message


# Function for asking questions - appending user messages to the chat logs before starting the `chat()` function
def ask(message):
    chat_messages.append(
        create_message(message, 'user')
    )
    print("\n\n--{message}--\n\n")
    return chat()  # Return the response


# Sending two example requests using the defined `ask()` function
response = ask('good morning')

# Now `response` variable contains the final answer from the assistant
print("Assistant's response:", response)
