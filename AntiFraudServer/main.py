from flask import Flask, request, Response
from dict2obj import Dict2Obj

import AntiFraudLogic
import logging
import database
import config
import PlatFormLists
import AntiFraudLogic
import AFRules

def get_user_config():
    return config.UserConfig

def get_app_config():
    return config.ApplicationConfig

def db_connect(user_config):
    db = database.DatabaseHandler(user_config)
    db.create_connection()
    return db

def getAFLogic():
    user_config = get_user_config()
    app_config = get_app_config()
    db = db_connect(user_config)
    pl = PlatFormLists.ListsHandler(db, app_config)
    pl.update_list_of_lists_and_content_from_db()
    rules = AFRules.rules
    channelList = ['Web']
    afLogic = AntiFraudLogic.AFLogic()
    afLogic.initializeContext(pl, rules, channelList)
    return afLogic

def main():
    afLogic = getAFLogic()
    
    app = Flask(__name__)
    @app.route('/transactions',methods = ["POST"])
    def parse_request():
        try:
            data = request.json
            transaction = Dict2Obj(data)
            response = afLogic.transactionHandler(transaction)
            return response
        except Exception as e:
            logging.error(e)
            return Response(response = "Bad message!", status = 503)

    app.run(debug=True,port=2000)

if __name__ == '__main__':
    main()