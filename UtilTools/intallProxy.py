from apptest import Card, GP
from apptest.TLV import LV
ProxyPackageAID = 'A000000333534254FF00000D'
ProxyInstanceAID = 'A0000003335342540000000D'
ProxyModuleAID = 'A0000003335342540000000D'
 

def installProxy(card):
    aid = ProxyInstanceAID
    card.Transmit('00A4040000') 
    gp = GP.GP('404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '0C')
    gp.Authentication(card, '01')
    gp.Delete(aid,card)
    p = 'C900' + 'EF'+ LV('A0'+LV('A5038201C0810101')+'CF'+LV('80'))
    gp.Install(ProxyPackageAID, ProxyModuleAID,ProxyInstanceAID, card,p,'00')#JCOP
        

if __name__ == '__main__':
    card = Card.Card()
    try:
        installProxy(card)
    except Exception ,e:
        print e
    else:
        print 'done!'
        