TRADE_MESSAGES = [ 'BUY' , 'SELL']
BANK_MESSAGES = [ 'REQUEST_LOAN', 'LOAN', 'BILL' ]

MESSAGES =


class Message(object):
    def __init__(self, code,values,sender = None, receiver = None):