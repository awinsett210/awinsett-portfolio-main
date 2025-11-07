from dotenv import load_dotenv

load_dotenv('./.env')

from langchain_ollama import ChatOllama
from langchain_core.prompts import (
                                        SystemMessagePromptTemplate,
                                        HumanMessagePromptTemplate,
                                        ChatPromptTemplate
                                        )
from langchain_core.output_parsers import StrOutputParser

base_url = "http://localhost:11434"
model = 'llama3.2:1b'

llm = ChatOllama(base_url=base_url, model=model)
llm

system = SystemMessagePromptTemplate.from_template('You are {drill} sargent. You answer in short sentences.')

question = HumanMessagePromptTemplate.from_template('tell me about the {trainings} in {points} points')

messages = [system, question]
template = ChatPromptTemplate(messages)

question = template.invoke({'drill': 'military', 'trainings': 'exercises', 'points': 3})


chain = template | llm | StrOutputParser ()
response = chain.invoke({'drill': 'military', 'trainings': 'exercises', 'points': 3})
print(response)

analysis_prompt = ChatPromptTemplate.from_template('''analyze the following text: {response}
                                                   You need tell me that how easy it is to understand.
                                                   Answer in two sentences only.
                                                   ''')


composed_chain = {"response": chain} | analysis_prompt | llm | StrOutputParser()

output = composed_chain.invoke({'drill': 'military', 'trainings': 'exercises', 'points': 3})
print(output)