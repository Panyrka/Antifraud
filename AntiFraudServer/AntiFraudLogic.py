from flask import Response
from config import UserConfig
from Interfaces import IListHandler
from Transaction import Transaction
from rule_result import rule_result
from rules import rule as active_rule
from round_time import round_to_sec

import flask_sqlalchemy
import logging

logging.basicConfig(level=UserConfig.logger_level)
logger = logging.getLogger('AFLogic')

class AFLogic:
    def __init__(self):
        self.context = {}
        self.flow = []
        pass
    
    def initializeContext(self, list_handler: IListHandler, rules, channelList):
        logger.debug('Initialize context')
        self.context['list_handler'] = list_handler
        self.context['channelLists'] = channelList
        self.context['rules'] = rules

    def checkChannel(self, transaction: Transaction):
        logger.debug('Check Transaction Started')
        if transaction.channel in self.context['channelLists']:
            logger.debug('Check Transaction Successfully Finished')
            return True, ''
        else:
            logger.error('Check Transaction Error: Transaction Channel')
            return False, 'Bad transaction channel!'
        
    def exec_rule(self, code, transaction, context):
        cont = {'transaction': transaction, 'context': context, 'result': None}
        exec(code, globals(), cont)
        print('here is: ', cont['result'])
        return cont['result']
    
    def checkRules(self, transaction, db):
        logger.debug('Check Rules Started')
        results = []
        rules = active_rule.query.all()
        print("\n----\n")
        for rule in rules:
            code = rule.code
            result = self.exec_rule(code, transaction, self.context)
            results.append([rule.name, rule.description, result])
        print("\n----\n")
        logger.debug('Check Rules Finished')
        return results

    def saveRulesResults(self, trx: Transaction, results, db):
        #logger.debug('For client ', transaction.clientName, ':')
        for r in results:
            print(r)
            res = rule_result(trx.transactionId, trx.normalizedDatetime, r[0], r[2])
            db.session.add(res)
            db.session.commit()

    def transactionHandler(self, data, db: flask_sqlalchemy.SQLAlchemy):
        transaction = Transaction.from_dict(data)
        transaction.normalizedDatetime = transaction.normalizedDatetime
        db.session.add(transaction)
        db.session.commit()
        
        successfully, desc = self.checkChannel(transaction)
        if not successfully:
            return Response(response=desc, status=503)
        
        rulesResult = self.checkRules(transaction, db)
        self.saveRulesResults(transaction, rulesResult, db)

        return Response(response = 'OK', status = 200)