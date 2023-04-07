def checkMoney(transaction, context):
    '''Описание правила'''
    ruleName = 'CheckMoney'
    description = 'Если сумма транзакции выше 1000'

    '''Условие правила'''
    print('checking rule ', ruleName)
    if transaction.normalizedAmount > 1000:
        return ruleName, description, True
    return ruleName, description, False

def isClientDeviceInBlackList(transaction, context):
    '''Описание правила'''
    ruleName = 'isClientDeviceInBlackList'
    description = 'Находится ли устройство клиента в БЛ'

    '''Условие правила'''
    print('checking rule ', ruleName)
    if context['list_handler'].exist_in_list('black_list_devices', transaction.deviceId):
        return ruleName, description, True
    return ruleName, description, False

def isIpInBlackList(transaction, context):
    '''Описание правила'''
    ruleName = 'isIpInBlackList'
    description = 'Находится ли IP в БЛ'

    '''Условие правила'''
    print('checking rule ', ruleName)
    if context['list_handler'].exist_in_list('black_list_ip', transaction.clientIp):
        return ruleName, description, True
    return ruleName, description, False

def isClientPhoneInBlackList(transaction, context):
    '''Описание правила'''
    ruleName = 'isClientPhoneInBlackList'
    description = 'Находится ли телефон клиента в БЛ'

    '''Условие правила'''
    print('checking rule ', ruleName)
    if context['list_handler'].exist_in_list('black_list_phones', transaction.phone):
        return ruleName, description, True
    return ruleName, description, False

def isClientAccountInBlackList(transaction, context):
    '''Описание правила'''
    ruleName = 'isClientAccountInBlackList'
    description = 'Находится ли счёт клиента в БЛ'

    '''Условие правила'''
    print('checking rule ', ruleName)
    if context['list_handler'].exist_in_list('black_list_account', transaction.payeeAccNumber):
        return ruleName, description, True
    return ruleName, description, False

rules = [checkMoney, isClientDeviceInBlackList, isIpInBlackList, isClientPhoneInBlackList, isClientAccountInBlackList]