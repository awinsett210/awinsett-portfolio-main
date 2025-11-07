import os
import tiktoken

from langchain_community.document_loaders import PyMuPDFLoader
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import (SystemMessagePromptTemplate, HumanMessagePromptTemplate,
                                    ChatPromptTemplate)
from langchain_core.output_parsers import StrOutputParser

load_dotenv('./.env')


loader = PyMuPDFLoader("datafiles/racing-in-america.pdf")
docs = loader.load()

len(docs)

pdfs = []
for root, dirs, files in os.walk("datafiles"):
    for file in files:
        if file.endswith(".pdf"):
            pdfs.append(os.path.join(root, file))

docs = []
for pdf in pdfs:
    loader = PyMuPDFLoader(pdf)
    temp = loader.load()
    docs.extend(temp)

len(docs)

def format_docs(docs):
    return "\n\n".join([x.page_content for x in docs])

context = format_docs(docs)

docs[0]

encoding = tiktoken.encoding_for_model("gpt-4o-mini")

encoding.encode("racing")
len(encoding.encode(docs[0].page_content))
len(encoding.encode(context))

base_url = "http://localhost:11434"
model = 'llama3.2:3b'

llm = ChatOllama(base_url=base_url, model=model)

system = SystemMessagePromptTemplate.from_template("""Answer user question based on the provided context. Do not answer in more than {words} words""")

prompt = """Answer user question based on the provided context ONLY! If you do not know the answer, just say "I don't know".
            ### Context:
            {context}

            ### Question:
            {question}

            ### Answer:"""

prompt = HumanMessagePromptTemplate.from_template(prompt)

messages = [system, prompt]
template = ChatPromptTemplate(messages)

qna_chain = template | llm | StrOutputParser()
qna_chain

response = qna_chain.invoke({'context': context, 'question': "What are the major forms of American auto racing?", 'words': 20})
print(response)
