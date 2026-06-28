import os
import json
import requests
from dotenv import load_dotenv

from tools import get_joke
from memory import load_memory, save_memory
from prompt import SYSTEM_PROMPT

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = "openai/gpt-oss-20b"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_joke",
            "description": "Fetch a random joke.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


def call_llm(messages):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "tool_choice": "auto"
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    return response.json()


def run_tool(tool_call):

    tool_name = tool_call["function"]["name"]

    # Remove unwanted suffix if added by the model
    tool_name = tool_name.split("<")[0].strip()

    if tool_name == "get_joke":
        return get_joke()

    return "Unknown tool."


def agent_loop(user_input):

    memory = load_memory()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(memory)

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = call_llm(messages)

    assistant = response["choices"][0]["message"]

    # If the model wants to use a tool
    if assistant.get("tool_calls"):

        tool_call = assistant["tool_calls"][0]

        joke = run_tool(tool_call)

        # Save conversation
        messages.append(assistant)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": joke
            }
        )

        save_memory(messages[1:])

        return joke

    # If no tool call
    answer = assistant.get(
        "content",
        "I'm a Joke Assistant and can only tell jokes."
    )

    save_memory(messages[1:])

    return answer


if __name__ == "__main__":


    print("=" * 60)
    print("😂 Welcome to the Joke Agent")
    print("=" * 60)
    print("I can tell you random jokes using a Joke API!")
    print()
    print("💬 Try asking:")
    print("  • Tell me a joke")
    print("  • Make me laugh")
    print("  • Tell me something humorous")
    print("  • Another joke")
    print("  • Random joke")
    print()
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:

            answer = agent_loop(user_input)

            print("\nAgent:", answer)

        except Exception as e:

            print("Error:", e)