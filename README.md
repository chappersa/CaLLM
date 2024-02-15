# climateGuide

--- PRE-REQUIREMENTS ---
Python3
Git

---LLAMA2 SET-UP---
To run the guide, we are required to have a local version of Meta's Llama2 LLM. To do this, clone the following two repositories into the directory:

1. git clone https://github.com/facebookresearch/llama.git
2. git clone https://github.com/ggerganov/llama.cpp.git

With both of these repositories cloned, navigate into llama.cpp and run the make command: make.

Next we want to request permission to access the Llama model by filling in the following form: https://ai.meta.com/resources/models-and-libraries/llama-downloads/

When you recieve an email from Meta with the unique download URL, copy this.

Follow the next steps to install and quantize your llama model:
1. Navigate into the llama repository
2. Run the download script: /bin/bash ./download.sh using your unique URL when asked for it
3. Specify the models you want to download (I recommend 13b-chat for this projects purposes)
4. Navigate to llama.cpp repository
5. Create a venv: python3 -m venv llama2
6. Activate venv: source llama2/bin/activate
7. Install requirements: python3 -m pip install -r requirements.txt
8. Convert the model to f16 format (the following command is for the 13b-chat model): python3 convert.py --outfile models/13B/ggml-model-f16.bin --outtype f16 ../../climateGuide/llama/llama-2-13b-chat --vocab-dir ../../climateGuide/llama
9. Quantize the model: 
./quantize  ./models/13B/ggml-model-f16.bin ./models/13B/ggml-model-q4_0.bin q4_0

Your local Llama model is now ready to use!


---ENVIRONEMENT VARAIBLES---
Open the .env file using your prefered text editor and add your versions of the following environment variables into the .env file:

OPENAI_API_KEY
APIFY_API_TOKEN
HUGGINGFACEHUB_API_TOKEN
PINECONE_API_TOKEN
PINECONE_ENV

---RUNNING GUIDE---
1. Navigate to climateGuide directory
2. Activate venv: source bin/activate
3. Install requirements: python3 -m pip install -r requirements.tx
4. Run guide: python3 app.py