'''
Created on Mar 13, 2017

@author: patrick
'''
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
# from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import pandas as pd
import pickle
from RandomForestGene import RandomForestGene

# from database_setup import Base, Music
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

############################################################################

class ClassificationManager():
    def __init__(self):
#         self.dynamodb=boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        self.dynamodb=boto3.resource('dynamodb', region_name='us-west-2')
        self.table=self.dynamodb.Table("AcceleratorData200Hz")
        self.classifier = pickle.load(open('ModingStatusClassification/forestStatus.pkl', 'rb'))
        self.walkSpeedClassifier = pickle.load(open('ModingStatusClassification/forestWalking.pkl', 'rb'))
        self.runSpeedClassifier = pickle.load(open('ModingStatusClassification/forestRunning.pkl', 'rb'))
#         self.classifier =''
#         self.walkSpeedClassifier =''
#         self.runSpeedClassifier =''
    
    
    def getAllDataFromDynamoDB(self):
        response = self.table.scan()
        arr=[]
        for item in response['Items']:
            line=item['info']['features']
            line=line.split(',')
            line.remove('')
            line.append(int(item['info']['speed']))
            if item['info']['type']=='sitting':
                line.append(0)
            elif item['info']['type']=='walking':
                line.append(1)
            else:
                line.append(2)
            arr.append(line)
        fr=pd.DataFrame(data=arr)
        
        col=[]
        for i in range(28):
            col.append(str(i))
        col.append('speed')
        col.append('types')
        fr.columns=col
        print(fr)
        return fr

    
    def trainRandomForest(self,pddata):
        train=RandomForestGene()
        traindata, testdata=train.dataspilit(pddata,0.8)
        forest=train.datatrainForType(traindata,numoftrees=500)
        with open('forestStatus.pkl', 'wb') as f:
            pickle.dump(forest, f)
        print("status classification training finished")


        walkdata=pddata[:][pddata["types"]==1]    
        traindata, testdata=train.dataspilit(walkdata,0.8)
        forest=train.datatrainForSpeed(traindata,numoftrees=500)
        with open('forestWalking.pkl', 'wb') as f:
            pickle.dump(forest, f)
        print("walking speed classification training finished")
        
        
        
        
        rundata=pddata[:][pddata["types"]==2]
        traindata, testdata=train.dataspilit(rundata,0.8)
        forest=train.datatrainForSpeed(traindata,numoftrees=500)
        with open('forestRunning.pkl', 'wb') as f:
            pickle.dump(forest, f)
        print("running speed classification training finished")
        self.classifier = pickle.load(open('forestStatus.pkl', 'rb'))
        self.walkSpeedClassifier = pickle.load(open('forestWalking.pkl', 'rb'))
        self.runSpeedClassifier = pickle.load(open('forestRunning.pkl', 'rb'))
        
        print("****************Forest Generation finished!*****************")

    def decideMovingStatus(self,data):
        preds = self.classifier.predict(data)
        if preds==0:
            return {"status":"sitting"}
        elif preds==1:
            return {"status":"walking"}
        elif preds==2:
            return {"status":"running"}
        else:
            return {"status":"error"}

    def decideWalkingSpeed(self,data):
        walkspeeds=[10,15,20,25,30,35]
        prob=self.walkSpeedClassifier.predict_proba(data)
        speed=0
        for i in range(len(prob[0])):
            speed=speed+prob[0][i]*walkspeeds[i]
        return {"speed":speed}
        
    def decideRunningSpeed(self,data):
        runspeeds=[25,30,35,40,45,50]
        prob=self.runSpeedClassifier.predict_proba(data)
        speed=0
        for i in range(len(prob[0])):
            speed=speed+prob[0][i]*runspeeds[i]
        return {"speed":speed}
    
    def decideStatusAndSpeed(self,data):
        status=self.decideMovingStatus(data)
#         print(status)
        if status["status"]=="sitting":
            return {"status":"sitting", "speed":0}
        elif status["status"]=="walking":
            # we need to change the speed to mile/h
            return {"status":"walking", "speed":float("%6.2f" %((self.decideWalkingSpeed(data)["speed"])/10))}
        elif status["status"]=="running":
            return {"status":"running", "speed":float("%6.2f" %((self.decideRunningSpeed(data)["speed"])/10))}
        else:
            return{"status":"error"}
        
        