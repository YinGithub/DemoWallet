from apptest import Card, GP
from Install import install  
from apptest.TLV import LV
def _parse(l,cfgDict):
    list_a = [e.replace('\n','') for e in l ]
    list_b = []
    for e in list_a:
        if 'AID' in e:
            e = e.replace('AID',cfgDict['AID'])
            e = e.replace('#','%02X'%(len(cfgDict['AID'])/2))
        list_b.append(e)
    return list_b

def _getPersoData(cfgDict):
    try:
        f = open('SZTPerso','r')
        fileList = f.readlines()
    finally:
        f.close()
    return _parse(fileList,cfgDict)

def perso(aid,card):
    cfgDict = {}
    cfgDict['AID'] = aid
    card.Transmit('00A40400'+LV(aid))
    gp = GP.GP('404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '0C')
    gp.Authentication(card, '03')
    perso_apdu_list  = _getPersoData(cfgDict)
    for i in perso_apdu_list[:-1]:
        print i
        gp.Send('80EC0001'+LV(LV(i)),card, expSW = '9000')
    gp.Send('80EC8001'+LV(LV(perso_apdu_list[-1])), card,expSW = '9000')

if __name__ == '__main__':
    aid  = '535A'
    card = Card.Card()
    #install(aid,card)
    #perso(aid,card)  
    print 'done'  
    
    
