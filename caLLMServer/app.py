import os
from flask import Flask, request
from caLLMVersions.GPUCaLLM import wakeUpCaLLM, runCaLLM
from repoManager import add, authenticated

callm = None
SEVER_PORT = os.environ["SERVER_PORT"] 
app = Flask(__name__)

@app.route('/')
def home():
    global callm 
    if callm is None:  
        callm = wakeUpCaLLM()
    return "CaLLM is awake"


@app.route("/getResponse")
def getResponse():
 if callm==None:
   print("ERROR: CaLLM is not awake")
 else:
    userText = request.args.get('msg') 
    response = runCaLLM(callm, userText)  
    return response    

@app.route("/addToRepo")
def addToRepo():
   data = request.args.get('url')
   status = add(data)
   return status

@app.route("/authenticate")
def authenticate():
   password = request.args.get('pas')
   status = authenticated(password)
   return status


if __name__ == "__main__":
    app.run(host='0.0.0.0', port= SEVER_PORT)