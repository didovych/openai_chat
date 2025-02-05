from store import Store
from carbon_footprint import CarbonFootprint
from asyncio import run

#from gpt_commands import GPTCommandsClient
from gpt_client.gpt_client import GPTClient

#CHAT_MODEL="gpt-3.5-turbo"
CHAT_MODEL="gpt-4o-mini"

def main():
    #manager = Store()
    manager = CarbonFootprint()

    gptClient = GPTClient(CHAT_MODEL, manager.system_prompt, manager)
    while True:
        prompt = input("You: ")
        print(gptClient.chat(prompt))

if __name__ == "__main__":
    run(main())