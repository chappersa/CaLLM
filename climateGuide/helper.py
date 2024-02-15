#Populating the vector database with relevant articles and information
import os
import pinecone
from dotenv import load_dotenv
from langchain_community.utilities import ApifyWrapper
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.document_loaders import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Pinecone
#from gtts import gTTS

load_dotenv()
PINECONE_API_TOKEN = os.environ["PINECONE_API_TOKEN"]
PINECONE_ENV = os.environ["PINECONE_ENV"]
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]
HF_EMBEDDINGS_MODEL_NAME = os.environ["HF_EMBEDDINGS_MODEL_NAME"]



#Scraping the articles on the provided site
def scrape(url):

    print("scraping:"+url+" ... ")

    apify = ApifyWrapper()
    loader = []

    loader = apify.call_actor(
        actor_id = "lukaskrivka/article-extractor-smart",
        run_input = {"startUrls": [{ "url": url }]},
        #Need to figure out this bit
        dataset_mapping_function = lambda item: Document(
            page_content=item["text"] or "", metadata={"source": item["url"]}
        ),
    )
    loader = loader.load()

    #Splitting the text into chunks 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1200,
        chunk_overlap  = 200
    )
    docs_chunks = text_splitter.split_documents(loader)

    #Initializing pinecone vector database
    pinecone.init(
        api_key = PINECONE_API_TOKEN,
        environment = PINECONE_ENV
    )

    index_name = PINECONE_INDEX_NAME
    embeddings_model_name = HF_EMBEDDINGS_MODEL_NAME
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    #create a new index
    vectorstore = Pinecone.from_documents(docs_chunks, embeddings, index_name=index_name)

    print("Scrape complete.")
    return vectorstore

def getVectorstore():
    pinecone.init(api_key=PINECONE_API_TOKEN,environment=PINECONE_ENV)
    embeddings = HuggingFaceEmbeddings(model_name=HF_EMBEDDINGS_MODEL_NAME)
    vectorstore = Pinecone.from_existing_index(PINECONE_INDEX_NAME, embeddings)
    return vectorstore


def text_to_speech(text):
    # Initialize gTTS with the text to convert
    speech = gTTS(text)

    # Save the audio file to a temporary file
    speech_file = 'response.mp3'
    speech.save(speech_file)

    # Play the audio file
   # os.system('aplay ' + speech_file)


