from flask import Blueprint
from flask import Flask, request, jsonify
import json
from ClassificationManager import ClassificationManager
# from time import sleep, time
# from sys import getsizeof

#init classifiers
classifier=ClassificationManager()


blah_bp=Blueprint('blah_bp',__name__, static_folder='static')

@blah_bp.route('/', methods=['GET'])
def loadHomePage():
    return blah_bp.send_static_file('index.html')

#reconstruct classifier on server
@blah_bp.route('/classification',methods=['GET'])
def reconstructClassifiers():
    df=classifier.getAllDataFromDynamoDB()
    classifier.trainRandomForest(df)
    return jsonify(**{"info":"update classifier success"})

@blah_bp.route('/classification/status',methods=['POST'])
def getStatusAndSpeed():
    data=request.get_json()
    print(data)
    features=[data['info']]
    res=classifier.decideStatusAndSpeed(features)
    print(res)
    return jsonify(**res)

