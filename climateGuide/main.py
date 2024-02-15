import os
import sys
import pinecone
from helper import scrape
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.vectorstores import Pinecone 
#from playsound import playsound

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]
HF_EMBEDDINGS_MODEL_NAME = os.environ["HF_EMBEDDINGS_MODEL_NAME"]
PINECONE_API_TOKEN = os.environ["PINECONE_API_TOKEN"]
PINECONE_ENV = os.environ["PINECONE_ENV"]
HF_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

user_input=input(f"Are you adding to the repository? y/n: ")
if user_input=='y':
    url=input(f"Please provide the url: ")
    vectorstore = scrape(url)
if user_input=='n':
    pinecone.init(api_key=PINECONE_API_TOKEN,environment=PINECONE_ENV)
    embeddings = HuggingFaceInferenceAPIEmbeddings(api_key = HF_API_TOKEN, model_name=HF_EMBEDDINGS_MODEL_NAME)
    vectorstore = Pinecone.from_existing_index(PINECONE_INDEX_NAME, embeddings)

prompt_template="""
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
You are a tour guide for varying age groups so make your answers short, informative and engaging.
Use the voice of a primary school teacher from Scotland.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs={"prompt": PROMPT}
callbacks = [StreamingStdOutCallbackHandler()]
config={'max_new_tokens':512,
                          'temperature':0,
                          'context_length':2048}
llm=CTransformers(model="model/ggml-model-q4_0.bin",
                  model_type="llama",
                  gpu_layers = 36,
                  config = config,
                  callbacks = callbacks)

qa = RetrievalQA.from_chain_type(
    llm = llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={'k': 2}),
    chain_type_kwargs=chain_type_kwargs,
    callbacks = callbacks
)

while True:
    user_input=input(f"Input Prompt: ")
    if user_input=='exit':
        print('Exiting')
        sys.exit()
    if user_input=='':
        continue
    print("Thinking...")
    result=qa.invoke({"query": user_input})
    response = result["result"]
    print('\n')

    #text_to_speech(response)
    #playsound('response.mp3')