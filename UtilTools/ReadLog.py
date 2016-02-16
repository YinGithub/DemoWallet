from apptest import Card
from lib.APDU import APDU
l = ['57414c4c45542e3031', '57414c4c45542e3032', '57414c4c45542e3033', '57414c4c45542e3034', '57414c4c45542e3035', '57414c4c45542e3036', '57414c4c45542e3037', '57414c4c45542e3038', '57414c4c45542e3039', '57414c4c45542e3130']

def ReadLog(aid):
    card  = Card.Card()
    apdu = APDU(card)
    apdu.selectAID(aid)
    apdu.selectFID('1001')
    for i in range(1,20):
        sfi = '18'
        apdu.updateRecord('00',sfi,23*'00',mode = '04')
        #apdu.readRecord('%02X'%i, sfi,'00')
        assert apdu.sw == '9000'


if __name__ == '__main__':
    aid = l[0]
    ReadLog(aid)
    
    
    
    