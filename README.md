# Project Summary

This project demonstrates the usage of the function calling functionality of the OpenAI. The [function calling documentation](https://platform.openai.com/docs/guides/function-calling).

## `GPTClient` Class

The `GPTClient` class is designed to interact with the OpenAI GPT models. It provides methods to send prompts to the model and receive generated responses. This class simplifies the process of integrating GPT-based functionalities into your applications.

### `Store` Example

The `Store` example demonstrates how to use the `GPTClient` class to simulate a conversation with a virtual store assistant. The assistant can help with product inquiries, provide recommendations, and assist with the checkout process. This example showcases the potential of integrating GPT models into e-commerce platforms to enhance customer experience.

### `CarbonFootprint` Example

The `CarbonFootprint` example illustrates the usage of the function calling with the public APIs. The [Carbon interface](https://docs.carboninterface.com/#/) is used for this example. To work with this API you need to add `CARBON_API_KEY` to your `.env` variables.