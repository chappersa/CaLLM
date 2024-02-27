#Populating the vector database with relevant articles and information
import os
import pinecone
import requests
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import Pinecone
from bs4 import BeautifulSoup
from pypdf import PdfReader
from pypdf.errors import PdfReadError

load_dotenv()

PINECONE_API_TOKEN = os.environ["PINECONE_API_TOKEN"]
PINECONE_ENV = os.environ["PINECONE_ENV"]
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]
HF_EMBEDDINGS_MODEL_NAME = os.environ["HF_EMBEDDINGS_MODEL_NAME"]
HF_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

def add(data):

    try:
        PdfReader(data)
    except PdfReadError:
        print("invalid PDF file")
        return 0
    else:
        #THIS WORKS FOR WIKI PAGES WHERE WE KNOW THE STRUCTURE
        #page = requests.get("https://en.wikipedia.org/wiki/Ballagan_Formation")
        #soup = BeautifulSoup(page.content, 'html.parser') 
        
        #title = soup.select("#firstHeading")[0].text
        #paragraphs = soup.select("p")
        #for para in paragraphs:
        #    print (para.text)

        #THIS WORKS FOR pdfs 
        loader = PyPDFLoader(data)
        pages = loader.load_and_split()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1200,
            chunk_overlap  = 200
        )

        docs_chunks = text_splitter.split_documents(pages)


        pinecone.init(
            api_key = PINECONE_API_TOKEN,
            environment = PINECONE_ENV
        )

        index_name = PINECONE_INDEX_NAME
        embeddings_model_name = HF_EMBEDDINGS_MODEL_NAME
        embeddings = HuggingFaceInferenceAPIEmbeddings(api_key = HF_API_TOKEN, model_name=embeddings_model_name)
        Pinecone.from_documents(docs_chunks, embeddings, index_name=index_name)

        print('Data added to the repository')
        return 1