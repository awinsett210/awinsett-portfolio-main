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
from langchain_core.runnables import RunnableLambda

base_url = "http://localhost:11434"
model = 'llama3.2:1b'

llm = ChatOllama(base_url=base_url, model=model)
llm

prompt = """Is the review below `Positive` or `Negative`.
            Only respond with one word.

            Review: {review}
            Classification:"""

template = ChatPromptTemplate.from_template(prompt)

chain = template | llm | StrOutputParser()

review = "Thank you so much! I happy with the service."

chain.invoke({'review': review})

#------------

pos_prompt = """
                Write a reply to a positive review.
                Review: {review}
                Answer:"""

pos_template = ChatPromptTemplate.from_template(pos_prompt)
pos_chain = pos_template | llm | StrOutputParser()

#----------------

neg_prompt = """
                Write a reply to a negative review. Encourage the user to report the issue further.
                Review: {review}
                Answer:"""


neg_template = ChatPromptTemplate.from_template(neg_prompt)
neg_chain = neg_template | llm | StrOutputParser()

#-----------------

def rout(info):
    if 'positive' in info['sentiment'].lower():
        return pos_chain
    else:
        return neg_chain
    
full_chain = {"sentiment": chain, 'review': lambda x: x['review']} | RunnableLambda(rout)

review = "I am very happy with this."

output = full_chain.invoke({'review': review})
print(output)
