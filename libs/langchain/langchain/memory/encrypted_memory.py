from langchain.memory import ConversationBufferMemory
from langchain.utils.encryption import encrypt

class EncryptedMemory(ConversationBufferMemory):
    def save_context(self, inputs: dict, outputs: dict) -> None:
        encrypted_input = encrypt(inputs.get(self.input_key, ""))
        inputs = {self.input_key: str(encrypted_input)}
        super().save_context(inputs, outputs)
