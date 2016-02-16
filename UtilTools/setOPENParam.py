from apptest import Card, GP
from lib.APDU import APDU
from apptest.TLV import LV
def _setOPEN():
    card = Card.Card()
    apdu = APDU(card)
    apdu.send('00A4040000')
    assert apdu.sw == '9000'
    gp = GP.GP('404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '0C')
    gp.Authentication(card, '01')
    gp.Send('80E64000'+LV('00000000'+LV('EF'+LV('A0'+LV('86'+LV('A0'+LV('80'+LV('0411223344')+'81'+LV('20')+'82'+LV('0800')+'83'+LV('02535A')+'84'+LV('C0')+'85'+LV('01')+'86'+LV('020200'))))))+'00'),card,'9000')

if __name__ == '__main__':
    _setOPEN()