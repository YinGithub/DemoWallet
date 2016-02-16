from apptest import Card
from lib.Terminal import Terminal
from lib import const,APDU, Util
from lib.Transaction import Transaction

l = ['57414c4c45542e3031', '57414c4c45542e3032', '57414c4c45542e3033', '57414c4c45542e3034', '57414c4c45542e3035', '57414c4c45542e3036', '57414c4c45542e3037', '57414c4c45542e3038', '57414c4c45542e3039', '57414c4c45542e3130']

class Key():
    def __init__(self,keyNo,keyValue):
        self.keyNo = keyNo
        self.keyValue = keyValue
class ADF():
    def __init__(self,aid,fid):
        self.aid = aid
        self.fid = fid
def test(card):
    aid = ''
    t = Terminal()
    ts = Transaction()
    for aid in [l[0]]:
        adf = ADF(aid,'1001')
        apdu = APDU.APDU(card)
        #t.tsAmount = '0000'+Util.generateRnd(2)
        t.tsAmount = '0009DFFF'
        t.tsType = const.TTI_EP_PURCHASE
        t.key = Key('01','0BA5B6D33FEC6DD73A5AA6CF81E818C7')
        ts.purchase(t, adf, apdu)
        
      

if __name__ == '__main__':
    card = Card.Card()
    test(card)
    
    
    
