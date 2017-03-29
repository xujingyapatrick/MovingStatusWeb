'''
Created on Mar 7, 2017

@author: patrick
'''
#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask, request, jsonify
import json
from ClassificationManager import ClassificationManager
# from time import sleep, time
# from sys import getsizeof

#init classifiers
classifier=ClassificationManager()

app = Flask(__name__,static_url_path='')


#get login page
@app.route('/', methods=['GET'])
def loadHomePage():
    return app.send_static_file('index.html')



#reconstruct classifier on server
@app.route('/classification',methods=['GET'])
def reconstructClassifiers():
    df=classifier.getAllDataFromDynamoDB()
    classifier.trainRandomForest(df)
    return jsonify(**{"info":"update classifier success"})

@app.route('/classification/status',methods=['POST'])
def getStatusAndSpeed():
    data=request.get_json()
    print(data)
    features=[data['info']]
    res=classifier.decideStatusAndSpeed(features)
    print(res)
    return jsonify(**res)




