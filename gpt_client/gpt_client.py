import json
from openai import OpenAI
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

from gpt_client.introspection import Manager, create_manager

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

    def __deepcopy__(self, memo):
        return self.value

@dataclass
class Message:
    role: Role
    content: str
    tool_call_id: Optional[str] = None

    def to_request(self) -> dict:
        result = {
            "role": self.role.value,
            "content": self.content,
        }

        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id

        return result

@dataclass
class FunctionExecution:
    id: str
    name: str
    arguments: Dict[str, str]

    def execute(self, manager: Manager) -> Optional[str]:
        return manager.execute(self.name, self.arguments)

class GPTClient:
    def __init__(
        self,
        model: str,
        system_prompt: str,
        manager: object,
    ):
        self.messages = [Message(Role.SYSTEM, system_prompt).to_request()]

        self.model = model
        self.system_prompt = system_prompt
        self.manager: Manager = create_manager(manager)
        self.openAIClient = OpenAI()

    def __send_message(self, message_to_send: Message) -> Optional[str]:
        self.messages.append(message_to_send.to_request())

        completion = self.openAIClient.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=[
                function.tool_json()
                for function in self.manager.functions.values()
            ],
        )

        # check if function call is present
        if completion.choices[0].message.tool_calls is not None:
            # TODO add support for multiple function calls
            # append model's function call message
            self.messages.append(completion.choices[0].message)

            # get function call from the completion
            function_call = self.__parse_function_call(completion.choices[0].message.tool_calls[0])

            function_result = function_call.execute(self.manager)

            return self.__send_message(Message(Role.TOOL, function_result, function_call.id))

        return completion.choices[0].message.content

    def __parse_function_call(self, tool_call: object) -> FunctionExecution:
        args = json.loads(tool_call.function.arguments)
        return FunctionExecution(tool_call.id, tool_call.function.name, args)

    def chat(self, prompt: str) -> str:
        """
        Sends a prompt to the OpenAI API and returns the response as a string

        Args:
            prompt: The prompt to send to the API

        Returns:
            The response from the API as a string
        """
        return self.__send_message(Message(Role.USER, prompt))