from flask import Response
from config import UserConfig
from Interfaces import IListHandler
from models import *
from round_time import round_to_sec

import flask_sqlalchemy
import logging
import Profile

logging.basicConfig(level=UserConfig.logger_level)
logger = logging.getLogger('AFLogic')

class AFLogic:
    def __init__(self):
        self.context = {}
        self.flow = []
        pass
    
    def initializeContext(self, list_handler: IListHandler, channelList, profiles_handler: Profile.ProfilesHandler):
        logger.debug('Initialize context')
        self.context['list_handler'] = list_handler
        self.context['channelLists'] = channelList
        self.context['profiles_handler'] = profiles_handler

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
        return cont['result']
    
    def checkRules(self, transaction, db):
        logger.debug('Check Rules Started')
        results = []
        rules = active_rule.query.all()
        print("Rules ", len(rules))
        for rule in rules:
            code = rule.code
            result = self.exec_rule(code, transaction, self.context)
            results.append([rule.name, rule.description, result, rule.rule_result_status])
            print(rule.name, result)
        print(results)
        logger.debug('Check Rules Finished')
        return results

    def saveRulesResults(self, trx: Transaction, results, db):
        #logger.debug('For client ', transaction.clientName, ':')
        for r in results:
            id = trx.transactionId
            date = trx.normalizedDatetime
            res = rule_result(id, date, r[0], r[2])
            db.session.add(res)
            db.session.commit()
    
    def write_profiles(self, trx: Transaction):
        profile_handler = self.context['profiles_handler']
        filters = profile_handler.get_filters()
        for filter in filters:
            result = self.exec_rule(filter['filter'], trx, self.context)
            print(filter['name'], result)
            if result:
                profile_handler.write(filter['name'], trx.normalizedAmount, trx.normalizedDatetime, trx.clientId)
                
    def generate_alerts(self, trx: Transaction, results, db):
        triggered_rules = ""
        is_decline = False
        for result in results:
            if result[2] == True:
                triggered_rules += result[0] + " "
                if result[3] == RULE_RESULT_STATUS.DECLINE:
                    is_decline = True
        if triggered_rules == "":
            return 'ALLOW'
        STATUS_CHOICES = ("FRAUD", "NEW", "LEGITIMATE")
        if is_decline:
            generated_alert = alert(trx.id, trx.clientId, trx.normalizedDatetime, triggered_rules, STATUS_CHOICES_ENUM.FRAUD)
            db.session.add(generated_alert)
            db.session.commit()
            return 'DECLINE'
        else:
            generated_alert = alert(trx.id, trx.clientId, trx.normalizedDatetime, triggered_rules, STATUS_CHOICES_ENUM.NEW)
            db.session.add(generated_alert)
            db.session.commit()
            return 'ALLOW'
    
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
        self.write_profiles(transaction)
        result = self.generate_alerts(transaction, rulesResult, db)
        return Response(response = result, status = 200)