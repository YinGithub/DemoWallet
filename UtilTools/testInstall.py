from apptest import Card, GP
from apptest.TLV import LV
from lib import Util
from Install import install
from Perso import perso
from UtilTools.InstallPBOC import _installPBOC
from UtilTools.persoForZYT import _persoForZYT
l = ['57414c4c45542e3031', '57414c4c45542e3032', '57414c4c45542e3033', '57414c4c45542e3034', '57414c4c45542e3035', '57414c4c45542e3036', '57414c4c45542e3037', '57414c4c45542e3038', '57414c4c45542e3039', '57414c4c45542e3130']

def test():
    card = Card.Card()
    
    try:
        _installPBOC(card)
        _persoForZYT(card)
        for i in range(0,9):
            aid = l[i]
            install(aid,card)
            perso(aid,card)
    except:
        print 'Error! Instance number : ',i

if __name__ == '__main__':
    test()
    print 'ok! '