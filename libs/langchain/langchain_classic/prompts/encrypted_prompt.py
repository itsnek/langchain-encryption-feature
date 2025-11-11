from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.messages import HumanMessage, SystemMessage
from typing import ClassVar, List, Any
from langchain_classic.utils.encryption import encrypt
import operator as op

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
DON'T GIVE REASONING OR EXPLAIN YOUR WAY OF THINKING. Just print the answers using the format indicated for LLM, "LLM: {...}"
User, Tool and LLM is only present in the examples to help you understand from whom does the response come. Don't include them in the answer.
"""
)

# Below you are provided with an example of the full transcript where your responses start with "LLM":
# User: {"Type": "ENCRYPTED", "Data": <DATA>}     ### <DATA> is of format b'...'
# LLM: {"Type": "TO-DECRYPT", "Data": <DATA>}     ### <DATA> is of format b'...'
# Tool: {"Type": "DECRYPTED", "Data": "Please translate to english: \"HOLA!\""}
# LLM: {"Type": "ANSWER", "Data" : "HELLO!"}
class EncryptedPromptTemplate(BasePromptTemplate):
    input_variables: List[str]
    _set_chat_history = ""

    def format(self, **kwargs: Any) -> str:
        user_input = kwargs.get("user_input", "")
        return encrypt(user_input)

    def format_prompt(self, **kwargs: Any) -> ChatPromptValue:
        dev_instructions = kwargs.get("dev_instructions", "")
        user_input = kwargs.get("user_input", "")
        chat_history = kwargs.get("chat_history", "")
        index = kwargs.get("index", 0)
        user_input = (
            encrypt(user_input) if index==0
            else user_input
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
        # print("CHAT_HISTORY_BEFORE: ", chat_history)
        # print("####")
        if chat_history == "":
            human_content = (
                f'{{"Type": "ENCRYPTED", "Data": "{str(user_input)}"}}'
            )
        elif op.contains(chat_history,"TO-DECRYPT"):
            human_content = (
                f'{{"Type": "DECRYPTED", "Data": "{user_input}"}}'
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
