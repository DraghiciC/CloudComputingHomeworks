import flask
import requests
import json
from flask import request, jsonify,session

app = flask.Flask(__name__)
app.config["DEBUG"] = True
e = open("C:\\Users\\Dan\\Desktop\\secretKey.txt", "r")
secretKey= e.read()
app.secret_key=secretKey
@app.route('/api/v1/resources/number', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "id required"
    l=0
    f = open("C:\\Users\\Dan\\Desktop\\superhero_token.txt", "r")
    key1= f.read()
    response=requests.get("https://superheroapi.com/api/"+key1+"/"+str(id)+"/powerstats")
    results=response.json()
    firstLetterCode=str(ord(results["name"][0]))
    l+=response.elapsed.total_seconds()
    print(l)
    g = open("C:\\Users\\Dan\\Desktop\\weather_token.txt", "r")
    key2= g.read()
    response=requests.get("http://api.openweathermap.org/data/2.5/weather?q=London&appid="+key2)
    results=response.json()
    temperature=str(int(results["main"]["temp"]))
    l+=response.elapsed.total_seconds()
    print(l)
    print(firstLetterCode,temperature)
    response=requests.get("http://www.randomnumberapi.com/api/v1.0/random?min="+firstLetterCode+"&max="+temperature+"&count=1")
    results=response.json()
    l+=response.elapsed.total_seconds()
    print(l)
    if "log" in session:
        log=session["log"]
    else:
        log=[]
    print(log)
    log.append((id,results[0],l))
    session["log"]=log
    return str(results[0])
@app.route('/api/v1/resources/metrics', methods=['GET'])
def api_metrics():
    log=session["log"]
    #session["log"]=[]
    return json.dumps(log)
app.run()