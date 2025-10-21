from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.prompts.chat import ChatPromptValue
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Any
from libs.langchain.langchain.utils.encryption import encrypt

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
