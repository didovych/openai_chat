from openai import OpenAI
from business_logic import *
import business_logic
import fileinput
import json

#CHAT_MODEL="gpt-3.5-turbo"
CHAT_MODEL="gpt-4o-mini"

def chat(client):
    completion = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "developer",
                "content": "You are a helpful assistant who is optimizing developer's daily tasks. Please try to be fun."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "To make this meeting more fun let's do the 'Word of the day' game. Peek an interesting word in Dutch and explain what does it mean."
                    }
                ]
            }
        ]
    )

    print(completion.choices[0].message)

    f = open("response_word.txt", "w", encoding='UTF8')
    f.write(completion.choices[0].message.content)
    f.close()

def text_to_voice(client):
    f = open("response_word.txt", "r", encoding='UTF8')
    text = f.read()
    print(text)

    # speech_file_path = "speech_word.mp3"
    # response = client.audio.speech.create(
    #     model="tts-1",
    #     voice="sage",
    #     input=text,
    # )
    # response.stream_to_file(speech_file_path)

def function_calling(message, client):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_order_status",
                "description": "Get the order status by order number.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_number": {
                            "type": "integer",
                            "description": "The customer's order number."
                        }
                    },
                    "required": ["order_number"],
                },
            },
        }
    ]

    completion = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "developer",
                "content": "You are an assistant for the online shop. You can use the 'get_order_status' and 'change_delivery_address' functions if you need."
            },
            {"role": "user", "content": message},
        ],
        tools=tools,
    )

    if completion.choices[0].message.content is not None:
        print(completion.choices[0].message.content)

    print('DEBUG START ***********************')
    print(completion.choices[0].message.tool_calls)
    print('DEBUG END *************************')

    if completion.choices[0].message.tool_calls is not None:
        fnName = completion.choices[0].message.tool_calls[0].function.name
        arguments = completion.choices[0].message.tool_calls[0].function.arguments
        status = handle_function_call(fnName, arguments)
        print('Your order status is: ' + status)

def handle_function_call(name, arguments):
    fn = getattr(business_logic, name)
    argJson = json.loads(arguments)
    return fn(argJson["order_number"])

client = OpenAI()

# completion.choices[0].message.tool_calls[0].function.name
# completion.choices[0].message.tool_calls[0].function.arguments
# {"order_number":546}

for line in fileinput.input():
    function_calling(line, client)