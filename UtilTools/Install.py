from apptest import Card, GP
from apptest.TLV import LV

SD_AID = 'A000000151000000'
SZT_PKG_AID = 'A000000333534254FF000010'
SZT_MDL_AID = 'A00000033353425400000010' 


def install(aid,card):
    card.Transmit('00A4040000') 
    gp = GP.GP('404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '0C')
    gp.Authentication(card, '01')
    gp.Delete(aid,card)
    p = 'C900' + 'EF'+ LV('A0'+LV('A5038201C0810101')+'CF'+LV('00'))
    #p = 'C900' 
    gp.Install(SZT_PKG_AID, SZT_MDL_AID, aid, card,p)

if __name__ == '__main__': 
    card = Card.Card()
    aid = '535A542E57414C4C45542E454E56'
    install(aid,card)
     