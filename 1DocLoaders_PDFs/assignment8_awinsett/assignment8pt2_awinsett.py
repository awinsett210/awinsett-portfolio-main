import os
import tiktoken

from langchain_community.document_loaders import PyMuPDFLoader
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import (SystemMessagePromptTemplate, HumanMessagePromptTemplate,
                                    ChatPromptTemplate)
from langchain_core.output_parsers import StrOutputParser

load_dotenv('./.env')


loader = PyMuPDFLoader("datafiles/History_of_Americas_speedways_past_present_-_2nd_ed_Comstock_Park_Mich.pdf")
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

system = SystemMessagePromptTemplate.from_template("""You are a document summarizer. You must not provide any false information.""")

prompt = """Summarize the given context in {words}.
            ### Context:
            {context}

            ### Summary:"""

prompt = HumanMessagePromptTemplate.from_template(prompt)

messages = [system, prompt]
template = ChatPromptTemplate(messages)

summary_chain = template | llm | StrOutputParser()
summary_chain

response = summary_chain.invoke({'context': context, 'words': 20})
print(response)