#Import Dependencies
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
from dotenv import load_dotenv,find_dotenv

#Load Environmental Variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

#Instantiate Finetuned LLM Model
llm=ChatOpenAI(model="ft:gpt-3.5-turbo-0125:personal:loansupport:9L2FZO36")

def create_indexing():
    #Loading PDF Data
    loader=PyPDFLoader('./data/loan-details.pdf')
    docs=loader.load()

    #Splitting Data
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=20
    )
    docs = text_splitter.split_documents(docs)

    #Create a Chroma Vector DB and Save
    db = Chroma.from_documents(docs,OpenAIEmbeddings(), persist_directory='./data/')
    

def create_retrieval():
    #Create Prompt Template
    prompt = ChatPromptTemplate.from_template("""
    You're operating as a loan support assistant for a bank. Your task is to assist users with inquiries regarding various loan products and processes. Keep responses concise and relevant. If the information requested is not available, do not provide any details.

    Question: {input}
    Context:
    {context}
    """)

    #Instantiate Document Chain
    document_chain=create_stuff_documents_chain(llm,prompt)

    #Load Vector DB
    db = Chroma(persist_directory='./data/', embedding_function=OpenAIEmbeddings())

    #Create a Retriever
    retriever = db.as_retriever()

    #Create Retrieval Chain
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    return retrieval_chain

if __name__ == "__main__":
    create_indexing()
    chain = create_retrieval()
    #print(chain.invoke({"input":"what do you know about areoplanes"}))