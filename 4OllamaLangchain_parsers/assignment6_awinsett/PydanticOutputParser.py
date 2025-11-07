from dotenv import load_dotenv

load_dotenv('./.env')

from langchain_ollama import ChatOllama
from langchain_core.prompts import (
                                        SystemMessagePromptTemplate,
                                        HumanMessagePromptTemplate,
                                        ChatPromptTemplate,
                                        PromptTemplate
                                        )
from typing import  Optional
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

base_url = "http://localhost:11434"
model = 'llama3.2:3b'

llm = ChatOllama(base_url=base_url, model=model)

class FunFact(BaseModel):
    """Fun Fact to tell user"""
    set: str = Field(description="The setup of the fun fact")
    fact: str = Field(description="The fun fact")
    rating: Optional[int] = Field(description="The rating of the fun fact from 1 to 10", default=None)

parser = PydanticOutputParser(pydantic_object=FunFact)

instruction = parser.get_format_instructions()

prompt = PromptTemplate(
    template='''
    Answer the user query with a fun fact. Here is your formatting instruction.
    {format_instruction}

    Query: {query}
    Answer:''',
    input_variables=['query'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

chain = prompt | llm | parser
output = chain.invoke({'query': 'Tell me a fun fact about a dog'})
print(output)