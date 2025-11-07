from dotenv import load_dotenv

load_dotenv('./.env')

from langchain_ollama import ChatOllama
from langchain_core.prompts import (
                                        SystemMessagePromptTemplate,
                                        HumanMessagePromptTemplate,
                                        ChatPromptTemplate
                                        )
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.runnables import chain

base_url = "http://localhost:11434"
model = 'llama3.2:1b'

llm = ChatOllama(base_url=base_url, model=model)
llm


def char_counts(text):
    return len(text)

def word_counts(text):
    return len(text.split())

prompt = ChatPromptTemplate.from_template("Describe these inputs in 3 sentences: {input1} and {input2}")

chain = prompt | llm | StrOutputParser()

output = chain.invoke({'input1': 'Staffordshire Bull Terrier is a dog', 'input2': 'Strawberry is a fruit'})

print(output)

chain = prompt | llm | StrOutputParser() | {'char_counts': RunnableLambda(char_counts), 
                                            'word_counts': RunnableLambda(word_counts), 
                                            'output': RunnablePassthrough()}

output = chain.invoke({'input1': 'Staffordshire Bull Terrier is a dog', 'input2': 'Strawberry is a fruit'})

print(output)
