from flask import Response
from config import UserConfig
from Interfaces import IListHandler

import logging

logging.basicConfig(level=UserConfig.logger_level)
logger = logging.getLogger('AFLogic')

class AFLogic:
    def __init__(self):
        self.context = {}
        pass
    
    def initializeContext(self, list_handler: IListHandler, rules, channelList):
        logger.debug('Initialize context')
        self.context['list_handler'] = list_handler
        self.context['channelLists'] = channelList
        self.context['rules'] = rules

    def checkChannel(self, transaction):
        logger.debug('Check Transaction Started')
        if transaction.channel in self.context['channelLists']:
            logger.debug('Check Transaction Successfully Finished')
            return True, ''
        else:
            logger.error('Check Transaction Error: Transaction Channel')
            return False, 'Bad transaction channel!'

    def checkRules(self, transaction):
        logger.debug('Check Rules Started')
        results = []
        for rule in self.context['rules']:
            result = rule(transaction, self.context)
            results.append(result)
        logger.debug('Check Rules Finished')
        return results

    def saveRulesResults(self, transaction, results):
        logger.debug('For client ', transaction.clientName, ':')
        for r in results:
            print(r)

    def transactionHandler(self, transaction):
        successfully, desc = self.checkChannel(transaction)
        if not successfully:
            return Response(response=desc, status=503)
        
        rulesResult = self.checkRules(transaction)
        self.saveRulesResults(transaction, rulesResult)

        return Response(response = 'OK', status = 200)