from apptest import Card
from lib.APDU import APDU
import os
def _persoForZYT(card):
    aid = 'A00000033301010600030800005A5954'
    apdu = APDU(card)
    apdu.selectAID(aid)
    apdu.gpInit('404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '0C')        
    apdu.gpAuth()
    path = os.getcwd()
    persoFp = open(path + '\\'+ "zytPerso.idf",'r')
    l = persoFp.readlines()
    l = [e.replace('\n','')for e in l]
    i = 0
    for e in l:
        i = i+1
        if 'DGI' in e:
            li =  e.split('=')
            dgi = li[0][3:]
            apduB = li[1]
            if i == len(l):
                last  = True
            else:
                last = False
            if (int(dgi,16)&0x8000 ) == 0x8000:
                encrypt = False
            else :
                encrypt = False
            apdu.gpStoreData(apduB, last, encrypt)
if __name__ == '__main__':
    card = Card.Card()
    _persoForZYT(card)