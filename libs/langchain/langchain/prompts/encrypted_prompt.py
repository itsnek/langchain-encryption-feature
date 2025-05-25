from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.prompts.chat import ChatPromptValue
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Any
from langchain.utils.encryption import encrypt
import base64

SYSTEM_INSTRUCTIONS = (
"""
To process the above instructions you will act as an assistant that communicates in JSON and supports two types of instructions. \
In the first type of instructions, user data is provided to you in the following format: \
User: {"Type": "ENCRYPTED", "Data": <DATA>}
This is encrypted data, which you will need to decrypt, using an external tool. \
To use the tool, output the received data in the following format: \
LLM: {"Type": "TO-DECRYPT", "Data": <DATA>}
The aforementioned tool, will provide you with the second type of instruction, that contains the decrypted user data. \
Please process the instruction found in the user data, the format of the second type of instruction is: \
Tool: {"Type": "DECRYPTED", "Data": <DecryptedDATA>}
Ones you have processed the instruction, return the answer in the following JSON format: \
LLM: {"Type": "ANSWER", "Data" : <AnswerDATA>}
"""
)
### input
### response
        # Below you are provided with an example of the full transcript where your responses start with "LLM":
        # User: {"Type": "ENCRYPTED", "Data": b'\x1e\x99_\x11\xb1{\x8b)\xd5;$\x1d4\x8e\xc5A\xe5B\xff;JL\x97\x0e\x16UKsg\x00\rSK\xa59\xcf(L\xd6I#\xfe4\x80x\xa5\xb0\x9d\xf0\x99\xd9\x85.7\x1d:\xea|\x07\xb1\xf5\xbb?\xe6\xf3\x8bE9T\xf3\xc1\xfb\x03\xdb\xf7\xd5f\xe5'}
        # LLM: {"Type": "TO-DECRYPT", "Data": b'\x1e\x99_\x11\xb1{\x8b)\xd5;$\x1d4\x8e\xc5A\xe5B\xff;JL\x97\x0e\x16UKsg\x00\rSK\xa59\xcf(L\xd6I#\xfe4\x80x\xa5\xb0\x9d\xf0\x99\xd9\x85.7\x1d:\xea|\x07\xb1\xf5\xbb?\xe6\xf3\x8bE9T\xf3\xc1\xfb\x03\xdb\xf7\xd5f\xe5'}
        # Tool: {"Type": "DECRYPTED", "Data": "Please translate to english: \"HOLA!\""}
        # LLM: {"Type": "ANSWER", "Data" : "HELLO!"}

class EncryptedPromptTemplate(BasePromptTemplate):
    input_variables: List[str]

    def format(self, **kwargs: Any) -> str:
        user_input = kwargs.get("user_input", "")
        encrypted = encrypt(user_input)

        return encrypted

    def format_prompt(self, **kwargs: Any) -> ChatPromptValue:
        dev_instructions = kwargs.get("dev_instructions", "")
        user_input = kwargs.get("user_input", "")
        chat_history = kwargs.get("chat_history", "")
        encrypted = (
            user_input if user_input.startswith("{\"decrypted_text\":")
            else encrypt(user_input)
        )

        if dev_instructions == "":
            system_content = (
                f"{SYSTEM_INSTRUCTIONS}\n"
            )
        else:
            system_content = (
                f"\nDeveloper's instructions: {dev_instructions}\nMiddleware's instructions:{SYSTEM_INSTRUCTIONS}"
            )

        human_content = ("")
        if chat_history == "":
            human_content = (
                f'User: {{"Type": "ENCRYPTED", "Data": "{str(encrypted)}"}}'
            )
        else:
            human_content = (
                f'Tool: {{"Type": "DECRYPTED", "Data": "{user_input}"}}'
            )
        system_message = SystemMessage(content=system_content)
        user_message = HumanMessage(content=human_content)

        return ChatPromptValue(messages=[system_message, user_message])

class BasicPromptTemplate(BasePromptTemplate):
    input_variables: List[str]

    def format(self, **kwargs: Any) -> str:
        user_input = kwargs.get("user_input", "")
        return user_input

    def format_prompt(self, **kwargs: Any) -> ChatPromptValue:
        dev_instructions = kwargs.get("dev_instructions", "")
        user_input = kwargs.get("user_input", "")
        chat_history = kwargs.get("chat_history", "")

        if dev_instructions == "":
            system_content = ("")
        else:
            system_content = (
                f"\nDeveloper's instructions: {dev_instructions}\n"
            )

        human_content = (
            f'{user_input}'
        )
        system_message = SystemMessage(content=system_content)
        user_message = HumanMessage(content=human_content)

        return ChatPromptValue(messages=[system_message, user_message])
