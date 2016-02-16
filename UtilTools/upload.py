from apptest import Card, GP
import os
SD_AID = 'A000000151000000'
SZT_PKG_AID = 'A000000333534254FF000010'
SZT_MDL_AID = 'A00000033353425400000010' 
def upload(card):
    gp = GP.GP()
    card.Transmit('00A4040000') 
    gp = GP.GP('404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '0C')
    gp.Authentication(card, '01')
    gp.Delete(SZT_PKG_AID, card, related = True)
    path = os.getcwd()
    cap_name = 'szt.cap'
    gp.load(SD_AID, path+ "\\" + cap_name, card)


if __name__ == '__main__':
    card = Card.Card()
    try:
        upload(card)
    except:
        print 'Error happened. '
    else:
        print 'ok !'
        