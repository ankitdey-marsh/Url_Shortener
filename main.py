from pymongo import MongoClient
import uuid
from flask import Flask,redirect,render_template

app=Flask(__name__)
client=MongoClient('mongodb://127.0.0.1:27017/')
db=client['url_shortener']
collection=db['storage']

@app.route('/sh/<path:url>',methods=['POST'])
def store_url(url):
    unique=str(uuid.uuid4())[:6]
    if collection.find_one({"Long":url}):
        shorter=collection.find_one({"Long":url})
        with open('text.txt','w') as f:
            f.write(shorter['Short'])
        return "Present",201,{'Access-Control-Allow-Origin': '*'}
    else:
        result=collection.insert_one({"Long":url,"Short":unique})
        shorter=collection.find_one({"Long":url})
        with open('text.txt','w') as f:
            f.write(shorter['Short'])
        if result.acknowledged:
            return "Value inserted",201,{'Access-Control-Allow-Origin': '*'}
        else:
            return "Insertion failed",400,{'Access-Control-Allow-Origin': '*'}

@app.route('/<string:url>',methods=['GET'])
def shorter_url(url):
    all=collection.find()
    for i in all:
        try:
            if url == str(i['Short']):
                return redirect(i['Long'],code=301)
        except:
            print("Some error occured")
    return 'Not found',404

if __name__=="__main__":
    app.run()

    