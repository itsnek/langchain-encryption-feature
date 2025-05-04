from typing import Dict, Any
from langchain_core.language_models.base import BaseLanguageModel
from langchain.chains.base import Chain
from langchain.prompts.encrypted_prompt import EncryptedPromptTemplate

class EncryptedInputChain(Chain):
    llm: BaseLanguageModel
    prompt_template: EncryptedPromptTemplate

    @property
    def input_keys(self):
        return ["user_input"]

    @property
    def output_keys(self):
        return ["response"]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, Any]:
        prompt = self.prompt_template.format(user_input=inputs["user_input"])
        response = self.llm.predict(prompt)
        return {"response": response}
