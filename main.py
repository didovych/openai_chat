from openai import OpenAI
from store import Store
from asyncio import run
from logging import getLogger

from gpt_client.client import GPTCommandsClient

#CHAT_MODEL="gpt-3.5-turbo"
CHAT_MODEL="gpt-4o-mini"

async def main():
    logger = getLogger(__name__)
    logger.info("Starting ...")

    system_prompt = """
        You are an assistant for the online shop.
    """

    manager = Store()

    # conversation examples:
    # Can you give me statuses of my orders under 180 euros?
    # What is the status of my order with the number FD4587?
    # Can you cancel my order with the number XX3322?

    model = CHAT_MODEL
    async with GPTCommandsClient(model, system_prompt) as client:
        while True:
            prompt = input("You: ")
            async for data in client.chat_stream(prompt, manager):
                print(data, end="")
            print()

if __name__ == "__main__":
    run(main())