import json
import os
from openai import OpenAI
from dotenv import load_dotenv

from tools import tools, available_functions

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent():
    # print("Hello Agent!")
    messages = [
        {"role": "system",
         "content": "You are a Financial assistant that answers questions about the exchange rate and stock prices."}
    ]

    print("Agent Started. Type 'exit' to quit.")

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_msg = response.choices[0].message
        tool_calls = response_msg.tool_calls

        if tool_calls:
            # print(response_msg)

            messages.append(response_msg)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                function_to_call = available_functions.get(function_name)

                if function_to_call:
                    try:
                        tool_result = function_to_call(**function_args)
                    except Exception as e:
                        tool_result = json.dumps({"error": str(e)})
                else:
                    tool_result = json.dumps({"error": "Function not found"})

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_result,
                })

            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )

            final_content = final_response.choices[0].message.content
            print(f"Assistant: {final_content}")
            messages.append({"role": "assistant", "content": final_content})
        else:
            print(f"Assistant: {response_msg.content}")
            messages.append({"role": "assistant", "content": response_msg.content})
if __name__ == "__main__":

    run_agent()
