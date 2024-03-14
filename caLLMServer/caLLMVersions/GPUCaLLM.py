import os
import sys
import pinecone
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
#from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.vectorstores import Pinecone
from accelerate import Accelerator
from repoManager import getVectorstore

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]
HF_EMBEDDINGS_MODEL_NAME = os.environ["HF_EMBEDDINGS_MODEL_NAME"]
PINECONE_API_TOKEN = os.environ["PINECONE_API_TOKEN"]
PINECONE_ENV = os.environ["PINECONE_ENV"]
HF_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]


def wakeUpCaLLM():
    vectorstore = getVectorstore()

    prompt_template="""
    Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    You are a tour guide for varying age groups so make your answers short (less than 100 words), informative and engaging.
    Use the voice of a primary school teacher from Scotland but do not use an accent. You do not work for NatureScot but have 
    some of their information in your data repository. Your name is CaLLM (pronounced Callum). 

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """

    PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    chain_type_kwargs={"prompt": PROMPT}
    accelerator = Accelerator()

    config={'max_new_tokens':512,
                            'temperature':0,
                            'context_length':2048, 'gpu_layers':43
                            }
    llm=CTransformers(model="model/ggml-model-q4_0.bin",
                    model_type="llama",
                    gpu_layers = 43,
                    config = config,
                    )
    llm, config = accelerator.prepare(llm, config)

    callm = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={'k': 3, 'score_threshold': 0.5}),
        chain_type_kwargs=chain_type_kwargs,
    )
    return callm


def runCaLLM(callm, user_input):

    result=callm.invoke({"query": user_input})
    response = result["result"]
    return response
