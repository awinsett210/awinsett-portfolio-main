from dotenv import load_dotenv

load_dotenv('./.env')

from langchain_ollama import ChatOllama
from langchain_core.prompts import (
                                        PromptTemplate
                                        )
from typing import  Optional
from pydantic import BaseModel, Field

base_url = "http://localhost:11434"
model = 'llama3.2:3b'

llm = ChatOllama(base_url=base_url, model=model)

class FunFact(BaseModel):
    """Fun Fact to tell user"""
    set: str = Field(description="The setup of the fun fact")
    fact: str = Field(description="The fun fact")
    rating: Optional[int] = Field(description="The rating of the fun fact from 1 to 10", default=None)

structured_llm = llm.with_structured_output(FunFact)

output = structured_llm.invoke('Tell me a fun fact about dirt track racing')
print(output)