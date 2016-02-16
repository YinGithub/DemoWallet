from apptest import Card
from apptest.TLV import LV
from lib.APDU import APDU
ProxyPackageAID = 'A000000333534254FF00000D'
ProxyInstanceAID = 'A0000003335342540000000D'
ProxyModuleAID = 'A0000003335342540000000D'
l = ['57414c4c45542e3031', '57414c4c45542e3032', '57414c4c45542e3033', '57414c4c45542e3034', '57414c4c45542e3035', '57414c4c45542e3036', '57414c4c45542e3037', '57414c4c45542e3038', '57414c4c45542e3039', '57414c4c45542e3130']

def _defaultSelect():
    card = Card.Card()
    apdu = APDU(card)
    apdu.selectFID('1001')
    assert apdu.sw == '9000'
    apdu.getBalance(True)
    assert apdu.sw == '9000'

if __name__ == '__main__':
    _defaultSelect()