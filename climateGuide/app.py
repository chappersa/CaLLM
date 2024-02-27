from flask import Flask, render_template, request, jsonify
from caLLMVersions.GPUCaLLM import wakeUpCaLLM, runCaLLM
from repoManager import add

callm = None

app = Flask(__name__)

@app.route('/')
def home():
    global callm 
    if callm is None:  
        callm = wakeUpCaLLM()
        print("CaLLM has been awoken")
    return render_template("index.html")


@app.route("/getResponse")
def getResponse():
 if callm==None:
    print("ERROR: CaLLM is not awake")
 else:
    userText = request.args.get('msg') 
    print(userText)
    response = runCaLLM(callm, userText)  
    print(response)
    response =  jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port= '31415')
    
@app.route("/addToRepo")
def addToRepo():
   data = request.args.get('url')
   status = add(data)
   message = None
   if status == 0:
      message = "Data could not be added"
   else:
      message = "Data successfully added!"
