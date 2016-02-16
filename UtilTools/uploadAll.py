
import os

from apptest import GP
from apptest.Card import Card
from lib.APDU import APDU


SD_AID = 'A000000151000000'
SZT_PKG_AID = 'A000000333534254FF000010'
SZT_MDL_AID = 'A00000033353425400000010' 

ProxyPackageAID = 'A000000333534254FF00000D'
interPackageAID = 'A000000333534254FF00000701'
interEventPackageAID = 'A000000333534254FF00000702'

PBOC_PKG_AID = 'B0004E5850050000000102'
PBOC_MDL_AID = 'B0004E585004D000000102' 
PPSE_PKG_AID = '325041592E'
PPSE_MDL_AID = '325041592E5359532E4444463031'
PPSE_AID = '325041592e5359532e4444463031'

SSPackageAID = 'A000000333534254FF000009'
pkg_path = r"C:\Users\xuyin\Desktop\DemoWallet\capFiles"

LoadELFDict =  {'0010':[SZT_PKG_AID,''],\
                'N000B':[ProxyPackageAID,''],\
                'N0008inter':[interPackageAID,''],\
                'N0008interEvent':[interEventPackageAID,''],\
                'PBOC':[PBOC_PKG_AID,''],\
                'ppse':[PPSE_PKG_AID,'']
                }

InstallSeq = ['ppse','N0008inter','N0008interEvent','N000B','0010','PBOC'] 
DeleteSeq = ['0010','PBOC','ppse','N000B','N0008interEvent','N0008inter']

def load(card,loadAll = False):
    apdu = APDU(card)
    dirList = os.listdir(pkg_path)
    itemList = LoadELFDict.keys()
    for e in dirList:
        for x in itemList:
            import re
            if re.search(x[:5]+'.*'+x[5:]+'$', e[:-4]):
                LoadELFDict[x][1] = e
    apdu.selectAID(SD_AID)
    
    gp = GP.GP('404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '404142434445464748494A4B4C4D4E4F', '0C')
    gp.Authentication(card, '01')
    if loadAll:
        for e in DeleteSeq:
            gp.Delete(LoadELFDict[e][0] ,card,related=True)
        for e in InstallSeq:
  
            gp.load(SD_AID,pkg_path+ "\\" + LoadELFDict[e][1],card)
    else:
        gp.Delete(LoadELFDict['0010'][0] ,card,related=True)
        gp.load(SD_AID,pkg_path+ "\\" + LoadELFDict['0010'][1],card)


if __name__ == '__main__': 
    card = Card() 
    load(card,True)
    print 'successful'