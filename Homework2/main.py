import flask
import requests
import json
from flask import request, jsonify,session,Response

import json

my_data = [
        {
            "id":"today",
            "content":"today's content",
            "date":"10/3/2021"
        },
        {
            "id":"yesterday",
            "content":"yesterday's content",
            "date":"9/3/2021"
        },
        {
            "id":"revelion",
            "content":"new year party",
            "date":"1/1/2021"
        },
        {
            "id":"vacanta",
            "content":"new country visited",
            "date":"4/5/2003"
        }
        ]

with open('personal.json', 'w') as json_file:
    json.dump(my_data, json_file)

app = flask.Flask(__name__)
app.config["DEBUG"] = True
e = open("C:\\Users\\Dan\\Desktop\\secretKey.txt", "r")
secretKey= e.read()
app.secret_key=secretKey

@app.route('/notes/today', methods=['GET'])
def function1():
    try:
        json_file = open('personal.json', 'r')
    except:
        return Response('internal server error', status=500)
    json_decode = json.load(json_file)
    for item in json_decode:
        if item['id']=='today':
            if len(item['content'])!=0:
                return Response(item['content'], status=200)
            else:
                return Response('content is empty', status=204)
    json_file.close()
    return Response("not found", status=404)

@app.route('/notes', methods=['GET'])
def function2():
    lim=0
    con=0
    try:
        json_file = open('personal.json', 'r')
    except:
        return Response('internal server error', status=500)
    json_decode = json.load(json_file)
    if 'limit' in request.args:
        try:
            int(request.args['limit'])
        except ValueError:
            return Response('bad request', status=400)
        lim=1
        limit = int(request.args['limit'])
    if 'content' in request.args:
        con=1
        content = request.args['content']
    l=[]
    for item in json_decode:
        if con==1 and not(item['content'].startswith(content)):
            continue
        l.append(item)
        if lim==1:
            limit-=1
            if limit==0:
                break
    json_file.close()
    if len(l)==0:
        return Response('content is empty', status=204)
    else:
        return Response(json.dumps(l), status=200)
@app.route('/notes', methods=['POST'])
def function3():
    try:
        json_file = open('personal.json', 'r')
    except:
        return Response('internal server error', status=500)
    json_decode = json.load(json_file)
    if 'id' in request.args and 'content' in request.args and 'date' in request.args:
        id = request.args['id']
        content = request.args['content']
        date = request.args['date']
    else:
        return Response('bad request', status=400)
    json_file.close()
    for item in json_decode:
        if item['id']==id:
            return Response('id already exists',status=409)
    json_file = open('personal.json', 'w')
    json_decode.append({"id":id,"content":content,"date":date})
    json.dump(json_decode, json_file)
    return Response('created', status=201)
@app.route('/notes/today', methods=['PUT'])
def function4():
    try:
        json_file = open('personal.json', 'r')
    except:
        return Response('internal server error', status=500)
    json_decode = json.load(json_file)
    if 'date' in request.args and 'content' in request.args:
        date = request.args['date']
        content = request.args['content']
    else:
        return Response('bad request', status=400)
    if len(content)==0:
        return Response('content is empty', status=204)
    l = []
    ok=0
    for item in json_decode:
        if item['id']=='today':
            item['content']=content
            item['date']=date
            ok=1
        l.append(item)
    json_file.close()
    json_file = open('personal.json', 'w')
    json.dump(l, json_file)
    json_file.close()
    if ok==1:
        return Response('ok', status=200)
    else:
        return Response("not found", status=404)
@app.route('/notes/today', methods=['DELETE'])
def function5():
    try:
        json_file = open('personal.json', 'r')
    except:
        return Response('internal server error', status=500)
    json_decode = json.load(json_file)
    l=[]
    ok=0
    for item in json_decode:
        if item['id']!='today':
            ok=1
            continue
        else:
            l.append(item)
    json_file.close()
    json_file = open('personal.json', 'w')
    json.dump(l, json_file)
    json_file.close()
    if ok==1:
        return Response('ok', status=200)
    else:
        return Response("not found", status=404)
@app.route('/notes', methods=['DELETE'])
def function6():
    try:
        json_file = open('personal.json', 'r')
    except:
        return Response('internal server error', status=500)
    a=0
    b=0
    c=0
    all=0
    if 'id' in request.args:
        a=1
        id = request.args['id']
    if 'content' in request.args:
        b=1
        content = request.args['content']
    if 'date' in request.args:
        c=1
        date = request.args['date']
    if 'all' in request.args:
        all=1
    if all==0 and a==0 and b==0 and c==0:
        return Response('bad request', status=400)
    json_decode = json.load(json_file)
    if len(json_decode)==0:
        return Response('not found', status=404)
    l=[]
    ok=0
    for item in json_decode:
        if a==1 and item['id'].startswith(id):
            ok=1
            continue
        if b==1 and item['content'].startswith(content):
            ok = 1
            continue
        if c==1 and item['date'].startswith(date):
            ok = 1
            continue
        if all==1:
            break
        l.append(item)
    json_file.close()
    json_file = open('personal.json', 'w')
    json.dump(l, json_file)
    json_file.close()
    if ok==1:
        return Response('ok', status=200)
    else:
        return Response("not found", status=204)
app.run()