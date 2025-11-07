from dotenv import load_dotenv

load_dotenv('./.env')

from langchain_ollama import ChatOllama
from langchain_core.prompts import (
                                        PromptTemplate
                                        )
from langchain_core.output_parsers import CommaSeparatedListOutputParser

base_url = "http://localhost:11434"
model = 'llama3.2:3b'

llm = ChatOllama(base_url=base_url, model=model)

parser = CommaSeparatedListOutputParser()

prompt = PromptTemplate(
    template='''
    Answer the user query with a list of nouns. Here is your formatting instruction.
    {format_instruction}

    Query: {query}
    Answer:''',
    input_variables=['query'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

chain = prompt | llm | parser
output = chain.invoke({'query': 'generate a list of nouns'})
print(output)