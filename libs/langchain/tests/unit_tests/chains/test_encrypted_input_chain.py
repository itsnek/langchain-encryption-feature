import pytest
from langchain.chains.encrypted_input_chain import EncryptedInputChain
from langchain.prompts.encrypted_prompt import EncryptedPromptTemplate
from langchain.llms.fake import FakeLLM

def test_encrypted_input_chain():
    llm = FakeLLM()
    prompt_template = EncryptedPromptTemplate(input_variables=["user_input","chat_history"],template="DUMMY")
    chain = EncryptedInputChain(llm=llm, prompt_template=prompt_template,memory=memory,verbose=True)
    
    response = chain.run(user_input="Test input.")
    print(response)
    response = chain.run(user_input="{\"decrypted_text\": \"Test input.\"}")
    print(response)

    assert response is not None
