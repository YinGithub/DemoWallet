from apptest import Card, GP
from apptest.TLV import LV, LV81
from lib.APDU import APDU
PKG_AID = '325041592E'
MDL_AID = '325041592E5359532E4444463031'
PPSE_AID = '325041592e5359532e4444463031'
def _installPPSE(card):
    card.Transmit('00A4040000') 
    gp = GP.GP('404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '0C')
    gp.Authentication(card, '01')
    aid = '325041592e5359532e4444463031'
   
    gp.Delete(aid,card)
    p = 'C900' + 'EF'+ LV('A0'+LV('A5038201C0810101'))
    P = 'C9038FF000EF0AA008810101A5038201C0'
    gp.Install(PKG_AID, MDL_AID, aid, card,p)
    apdu = APDU(card)
    apdu.selectAID(PPSE_AID)
    apdu.gpInit('404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '0C')        
    apdu.gpAuth()
    DGI9102_PPSE = '9102'+LV('A5'+LV81('BF0C'+LV('61'+LV('4F'+LV('A00000033301010600030800005A5954')+'50'+LV('50424F435F437265646974')+'870101'))))

    apdu.gpStoreData(DGI9102_PPSE, last = True)
if __name__ == '__main__': 
    card = Card.Card()
    _installPPSE(card)   
    
    
   
