
###
<div align="center">
  <img height="400" src="CaLLM.png"  />
</div>

###

<h1 align="left">CaLLM Server and Plug-in</h1>

###

<p align="left">This is the implementation of my CS4098 Minor Software Project that provides the server and a Word Press plug-in front-end for a climate conscious chat bot that can be given specialised knowledge by adding to the information repository it is using to answer questions in an informed way. <br>It uses ggerganov's llama.cpp quantised model as the LLM and the Retrieval Augmented Generation (RAG) technique to provide context specific information. Langchain, Hugging Face and Pinecone are used to build the RAG chain. </br> </p>

###

<h2 align="left">Pre-Requisits</h2>

###

<p align="left">Python3<br>Git</p>

###

<h2 align="left">Llama Model Set-up</h2>

###

<p align="left">To run the guide, we need to have a quantised version of Meta's Llama2 LLM locally. To do this, clone the following two repositories into the caLLMServer directory:<br><br>1. git clone https://github.com/facebookresearch/llama.git<br>2. git clone https://github.com/ggerganov/llama.cpp.git<br><br>With both of these repositories cloned, navigate into llama.cpp and run the make command: make.<br><br>Next we want to request permission to access the Llama model by filling in the following form: https://ai.meta.com/resources/models-and-libraries/llama-downloads/<br><br>When you receive an email from Meta with the unique download URL, copy this.<br><br>Follow the next steps to install and quantize your llama model:<br>1. Navigate into the llama repository<br>2. Run the download script: /bin/bash ./download.sh using your unique URL when asked for it<br>3. Specify the models you want to download (I recommend 13b-chat for this projects purposes)<br>4. Navigate to llama.cpp repository<br>5. Create a venv: python3 -m venv llama2<br>6. Activate venv: source llama2/bin/activate<br>7. Install requirements: python3 -m pip install -r requirements.txt<br>8. Convert the model to f16 format (the following command is for the 13b-chat model): python3 convert.py --outfile models/13B/ggml-model-f16.bin --outtype f16 ../../caLLMServer/llama/llama-2-13b-chat --vocab-dir ../../caLLMServer/llama<br>9. Quantize the model: <br>./quantize  ./models/13B/ggml-model-f16.bin ./models/13B/ggml-model-q4_0.bin q4_0<br><br>Create a directory in the /caLLMServer directory called /model.<br>Move the ggml-model-q4_0.bin q4_0 file into the model directory in /climateGuide. <br>The llama and llama.cpp directories can now be deleted.<br><br>Your local Llama model is now ready to use!</p>

###

<h2 align="left">Word Press Plug-in</h2>

###

<p align="left">The WP Plug-in is stored in the directory \CaLLMPlugin. This can be zipped and uploaded to a Word Press site as a plug-in and included as shortcode. <br><br>Ensure that you change the query.php file to point to your server.</p>

###

<div align="center">
  <img height="200" src="https://en-support.files.wordpress.com/2023/10/shortcode-block-slash-command.png"  />
</div>

###

<h2 align="left">Environment Variables</h2>

###

<p align="left">Open the .env file using your preferred text editor and add your versions of the following environment variables into the .env file:<br><br>HUGGINGFACEHUB_API_TOKEN = (Your Hugging Face Hub API key)<br>HF_EMBEDDINGS_MODEL_NAME = (The Hugging Face model embeddings name you want to use) <br>PINECONE_API_TOKEN = (Your Pinecone vector database API key) <br>PINECONE_ENV = (The Pinecone environment of your vector database)<br>PINECONE_INDEX_NAME = (The index of the Pinecone vector database) <br>ADMIN_PASSWORD = (Your admin password for adding information to the repository) <br>SERVER_PORT = (The server port number to run the back end)</p>

###

<h2 align="left">Server Running Guide</h2>

###

<p align="left">1. Navigate to /caLLMServer directory<br>2. Activate venv: source bin/activate<br>3. Install requirements: python3 -m pip install -r requirements.tx<br>4. Run server: python3 app.py</p>

###
