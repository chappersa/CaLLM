#Populating the vector database with relevant articles and information
import os
import pinecone
import requests
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import Pinecone
from pypdf import PdfReader
from urllib.parse import urlparse


load_dotenv()
#Get the environment variables (should be set in the .env)
PINECONE_API_TOKEN = os.environ["PINECONE_API_TOKEN"]
PINECONE_ENV = os.environ["PINECONE_ENV"]
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]
HF_EMBEDDINGS_MODEL_NAME = os.environ["HF_EMBEDDINGS_MODEL_NAME"]
HF_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

#Add data to the repository
def add(data):
    wiki = False
    pdf = False

    if not os.path.exists(data):
            
        try:
            response = requests.head(data)
            if response.status_code == 200:
                if data.startswith("https://en.wikipedia.org"):
                    wiki = True
                    pass
                else:
                    error = data + " is not a wikipedia page!"
                    return error
                
        except requests.ConnectionError as e:  # Catching a subclass of BaseException
            error = (f"Could not connect to the website {data}: {e}")
            return error
        except Exception as e:  # Catching a subclass of BaseException
            error = (f"An error occurred: {e}")
            return error
    else:
        error = "File does not exist"
        return error
    

    if os.path.exists(data):
        try:
            with open(data, 'rb') as file:
                PdfReader(file)
                pdf = True
        except Exception as e:
            print("Error:", e)
            error = "Invalid PDF file"
            return error

    if pdf:
        
        loader = PyPDFLoader(data)
        pages = loader.load()

    if wiki:
        wikiPage = urlparse(data)
        pageName = wikiPage.path.split('/')[-1]
        loader = WikipediaLoader(pageName, 'en', 1) 
        pages = loader.load()

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

    success = "Data successfully added to the repository"
    return success

#Check the user has the correct password, set in the .env file
def authenticated(password):
    if(password == ADMIN_PASSWORD):
        return "correct"
    else:
        return "incorrect"

#Get the vector database using the keys in the .env file
def getVectorstore():
    pinecone.init(api_key=PINECONE_API_TOKEN,environment=PINECONE_ENV)
    embeddings_model_name = HF_EMBEDDINGS_MODEL_NAME
    embeddings = HuggingFaceInferenceAPIEmbeddings(api_key = HF_API_TOKEN, model_name=embeddings_model_name)
    vectorstore = Pinecone.from_existing_index(PINECONE_INDEX_NAME, embeddings)
    return vectorstore
