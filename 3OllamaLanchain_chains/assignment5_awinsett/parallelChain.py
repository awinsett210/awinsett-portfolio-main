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

#--------------------------

system = SystemMessagePromptTemplate.from_template('You are {drill} sargent. You answer in short sentences.')

question = HumanMessagePromptTemplate.from_template('tell me about the {trainings} in {points} points')


messages = [system, question]
template = ChatPromptTemplate(messages)
fact_chain = template | llm | StrOutputParser()

output = fact_chain.invoke({'drill': 'military', 'trainings': 'exercises', 'points': 3})
print(output)


question = HumanMessagePromptTemplate.from_template('write a paragraph on {trainings} in {sentences} lines')

messages = [system, question]
template = ChatPromptTemplate(messages)
paragraph_chain = template | llm | StrOutputParser()

output = paragraph_chain.invoke({'drill': 'military', 'trainings': 'exercises', 'sentences': 4})
print(output)

chain = RunnableParallel(fact = fact_chain, paragraph = paragraph_chain)

output = chain.invoke({'drill': 'military', 'trainings': 'exercises', 'points': 3,'sentences': 4})
print(output['fact'])
print('\n\n')
print(output['paragraph'])


