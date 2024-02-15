from flask import Flask, render_template, request, jsonify
from chat import wakeUpCaLLM, runCaLLM

callm = 0

app = Flask(__name__)

@app.route('/')
def home():
    global callm 
    callm = wakeUpCaLLM()
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
 if callm==0:
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
    app.run(host='0.0.0.0', port= '5000')
    

