from flask import Flask,request,render_template,redirect, Response
from werkzeug.utils import secure_filename
from dict2obj import Dict2Obj
from rules import *

import os
import glob
import json
import logging

app = Flask(__name__)

channelList = ['Web']

def checkChannel(transaction):
    print('Check Transaction Started')
    if transaction.channel in channelList:
        print('Check Transaction Successfully Finished')
        return True, ''
    else:
        print('Check Transaction Error: Transaction Channel')
        return False, 'Bad transaction channel!'

def checkRules(transaction):
    print('Check Rules Started')
    results = []
    for rule in rules:
        result = rule(transaction)
        results.append(result)
    print('Check Rules Finished')
    return results

def saveRulesResults(transaction, results):
    print('For client ', transaction.clientName, ':')
    for r in results:
        print(r)

def transactionHandler(transaction):
    successfully, desc = checkChannel(transaction)
    if not successfully:
        return Response(response=desc, status=503)
    
    rulesResult = checkRules(transaction)
    saveRulesResults(transaction, rulesResult)

    return Response(response = 'OK', status = 200)

@app.route('/transactions',methods = ["POST"])
def parse_request():
    try:
        data = request.json
        transaction = Dict2Obj(data)
        response = transactionHandler(transaction)
        return response
    except Exception as e:
        logging.error(e)
        return Response(response = "Bad message!", status = 503)

app.run(debug=True,port=2000)