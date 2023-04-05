from lists import *

def checkMoney(transaction):
    '''Описание правила'''
    ruleName = 'CheckMoney'
    description = 'Если сумма транзакции выше 1000'

    '''Условие правила'''
    print('checking rule ', ruleName)
    if transaction.normalizedAmount > 1000:
        return ruleName, description, True
    return ruleName, description, False

def isFL(transaction):
    '''Описание правила'''
    ruleName = 'isClientFl'
    description = 'Явялется ли клиент ФЛ'

    '''Условие правила'''
    print('checking rule ', ruleName)
    if transaction.transactionType == 'FL':
        return ruleName, description, True
    return ruleName, description, False

def isClientPhoneInBlackList(transaction):
    '''Описание правила'''
    ruleName = 'isClientPhoneInBlackList'
    description = 'Находится ли телефон клиента в БЛ'

    '''Условие правила'''
    print('checking rule ', ruleName)
    if transaction.phone in PhonesBL:
        return ruleName, description, True
    return ruleName, description, False

def clientCardType(transaction):
    '''Описание правила'''
    ruleName = 'clientCardType'
    description = 'Определение типа карты клиента'
    
    '''Условие правила'''
    print('checking rule ', ruleName)
    if transaction.cardKey[0] == '2':
        return ruleName, description, 'MIR'
    if transaction.cardKey[0] == '4':
        return ruleName, description, 'VISA'
    if transaction.cardKey[0] == '5':
        return ruleName, description, 'MS'
    return ruleName, description, 'UF'

rules = [checkMoney, isFL, isClientPhoneInBlackList, clientCardType]