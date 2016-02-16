# -*-encoding:utf-8-*-
'''
@auth Yin.Xu
'''

from apptest import GP
from apptest.Algorithm import Algo_MAC, Algo_DES_Encryption_ECB, Algo_Xor
from apptest.Card import CheckIf
from apptest.TLV import LV

import const 



class APDU():
    def __init__(self,card):
        self.card = card
        self.sw = ''
        self.sw1 = ''
        self.sw2 = ''
        self.res = ''
        self.checkSW = False
        self.gp = GP.GP(const.GP_K1,const.GP_K2,const.GP_K3,const.GP_KVER)
        self.apdu = ''
        self.isGPApdu = False
        self.apduList = []
        self.timeList = []
        self.collectTime = False
    def setCheckSW(self):
        self.checkSW = True
    def setNotCheckSW(self):
        self.checkSW = False
    def setCollectTransactionTime(self):
        self.collectTime = True
        self.timeList = []
    def getTimeList(self):
        return self.timeList
        
    def selectAID(self,aid):
        self.apdu = '00A40400' + LV(aid)
        self.postProcess()
    def selectFID(self,fid):
        self.apdu = '00A40000' + LV(fid)
        self.postProcess() 
    def createFile(self,fid, apduB):
        self.apdu = '80E0' + fid + LV(apduB)
        self.postProcess()
    def getChallenge(self,le):
        self.apdu = '00840000' + le
        self.postProcess()
    def initForLoad(self,isEP,keyIndex, amount, terminalNumber):
        if isEP:
            self.apdu = ('80500002' + LV(keyIndex + amount + terminalNumber))
        else:
            self.apdu = ('80500001' + LV(keyIndex + amount + terminalNumber))
        self.postProcess()
    def initForPurchase(self,isEP,keyIndex, amount, terminalNumber):
        if isEP:
            self.apdu =  '80500102' + LV(keyIndex + amount + terminalNumber)
        else:
            self.apdu =  '80500101' + LV(keyIndex + amount + terminalNumber)
        self.postProcess()
        
    def initForCappLoad(self,isEP,keyIndex, amount, terminalNumber):
        if isEP:
            self.apdu = '80500602' + LV(keyIndex + amount + terminalNumber)
        else:
            self.apdu = '80500601' + LV(keyIndex + amount + terminalNumber)

        
    def creditForLoad(self,dateTime,mac2):
        self.apdu = '80520000' + LV(dateTime + mac2)
        self.postProcess()
        
    def debitForPurchase(self,terminalCounter, dateTime, mac1):
        self.apdu =  '80540100' + LV(terminalCounter + dateTime + mac1)
        self.postProcess()
    
 
    def send(self,apdu):
        self.apdu = apdu
        self.postProcess()
    def gpInit(self,k1,k2,k3,kVer):
        self.gp = GP.GP(k1,k2,k3,kVer)
    
    def applicationBlock(self,isTemporary,rand, key):
        if isTemporary:
            cmd = '841E000004'
        else:
            cmd = '841E000104'
        self.apdu = cmd + Algo_MAC(cmd, rand, key)[:8]
        self.postProcess()
    def getTransactionProve(self,tsType, tsCtr):
        self.apdu = '805A00' + tsType + LV(tsCtr) 
        self.postProcess()
    def getBalance(self,isEP):
        if isEP:
            self.apdu  = '805C000204'
        else:
            self.apdu = '805C000104'
        self.postProcess()
    
    def gpSend(self,apdu):
        self.apdu = apdu
        self.isGPApdu = True
        self.res,self.sw  = self.gp.Send(apdu,self.card)  
    def gpAuth(self,secLevel = '01'):
        self.gp.Authentication(self.card, secLevel)
        self.isGPApdu = True
    def gpStoreData(self, data, last = False, encrypt = False):
        self.res,self.sw = self.gp.StoreData(data, self.card, last, encrypt)
        assert self.sw == '9000'
        self.isGPApdu = True
    def readBianry(self,sfi, offset, le,key = '',iv = ''):
        if key != '':
            cmd  = '04B0' + '%02X' % (int(sfi, 16) + 0x80) + offset + '04'
            self.apdu =  cmd + Algo_MAC(cmd, iv, key)[:8]
        else:
            self.apdu = '00B0' + '%02X' % (int(sfi, 16) + 0x80) + offset + le
        self.postProcess()
    def updateBinary(self,sfi, offset, data, key='', iv=''):
        if key == '':
            cmd = '00D6' + '%02X' % (int(sfi, 16) + 0x80) + offset + LV(data)
        else:
            cmd =  '04D6' + '%02X' % (int(sfi, 16) + 0x80) + offset + '%02X' % (len(data) / 2 + 4) + data
            cmd =  cmd + Algo_MAC(cmd, iv, key)[:8]
        self.apdu = cmd
        self.postProcess()
        
    def readRecord(self,p1, sfi,le,mode=4,key = '',iv = ''):
        # mode 4 as No,mode 0 as tag
        if key !=  '':
            cmd = '04B2' + p1 + '%02X' % (int(sfi, 16) * 8 + mode) + '04'
            self.apdu = cmd + Algo_MAC(cmd, iv, key)[:8]
        else :
            self.apdu =  '00B2' + p1 + '%02X' % (int(sfi, 16) * 8 + mode) + le    
        self.postProcess()

    
    def updateRecord(self,p1, sfi, data,mode = '04',key='', iv=''):
        # mode 4 as No
        # mode 0 as tag`
        p2 = '%02X'%((int(sfi,16)<<3)  + int(mode,16))
        if key == '':
            cmd =  '00DC' + p1 + p2 + LV(data)
        else:
            cmd = '04DC' + p1 + p2 + '%02X' % (len(data) / 2 + 4) + data
            cmd = cmd + Algo_MAC(cmd, iv, key)[:8]
        self.apdu = cmd 
        self.postProcess()

    
    def writeKey(self,p1, p2, keyData, key='', iv=''):
        if key == '':
            cmd = '80D4' + p1 + p2 + LV(keyData)
        else:
            keyData = LV(keyData) + '80'
            while len(keyData) % 16 != 0:
                keyData += '00'
            keyData = Algo_DES_Encryption_ECB(keyData, key)
            cmd = '84D4' + p1 + p2 + '%02X' % (len(keyData) / 2 + 4) + keyData
            cmd = cmd + Algo_MAC(cmd, iv, key)[:8]
        self.apdu = cmd 
        self.postProcess()

    
    def appendRecord(self,sfi, data, key='', iv=''):
        if key == '':
            cmd = '00E200' + '%02X' % (int(sfi, 16) * 8) + LV(data)
        else:
            cmd = '04E200' + '%02X' % (int(sfi, 16) * 8) + '%02X' % (len(data) / 2 + 4) + data
            cmd = cmd + Algo_MAC(cmd, iv, key)[:8]
        self.apdu = cmd 
        self.postProcess()
    

    
    def initializeForCappLoad(self,keyIndex, amount, terminalNumber):
        cmd = '80501002' + LV(keyIndex + amount + terminalNumber)
        self.apdu = cmd 
        self.postProcess()
    
    def initializeForLoad(self,isEP, keyIndex, amount, terminalNumber):
        if isEP:
            cmd = '80500002' + LV(keyIndex + amount + terminalNumber)
        else:
            cmd = '80500001' + LV(keyIndex + amount + terminalNumber)
        self.apdu = cmd 
        self.postProcess()
    
    def initializeForPurchase(self,isEP, keyIndex, amount, terminalNumber):
        if isEP:
            cmd = '80500102' + LV(keyIndex + amount + terminalNumber)
        else:
            cmd = '80500101' + LV(keyIndex + amount + terminalNumber)
        self.apdu = cmd 
        self.postProcess()
    
    def initializeForCappPurchase(self,keyIndex, amount, terminalNumber):
        cmd = '80500302' + LV(keyIndex + amount + terminalNumber)
        self.apdu = cmd 
        self.postProcess()
    def initializePurchaseWithLoyalty(self,keyIndex, amount, terminalNumber, bonusRate):
        cmd = '80501102' + LV(keyIndex + amount + terminalNumber + bonusRate)
        self.apdu = cmd 
        self.postProcess()
    def deibtForPurchase(self,terminalCounter, dateTime, mac1):
        cmd = '80540100' + LV(terminalCounter + dateTime + mac1)
        self.apdu = cmd 
        self.postProcess()
    def updateCappBinaryCache(self,sfi, offset, data):
        cmd = '80D6' + '%02X' % (int(sfi, 16) + 0x80) + offset + LV(data)
        self.apdu = cmd 
        self.postProcess() 
    def updateCappDataCache(self,tag, sfi, data):
        cmd = '80DC' + tag + '%02X' % (int(sfi, 16) * 8) + LV(data)
        self.apdu = cmd 
        self.postProcess()
    def verifyPin(self,pin):
        if len(pin) % 2 != 0:
            pin += 'F'
        cmd = '00200000' + LV(pin)
        self.apdu = cmd 
        self.postProcess()
    def unblockPin(self,pin, randData, key):
        if len(pin) % 2 != 0:
            pin += 'F'
        pin = LV(pin) + '80'
        pin += '0' * (16 - len(pin))
        pin = Algo_DES_Encryption_ECB(pin, key)
        cmd = '842400000C' + pin
        cmd = cmd + Algo_MAC(cmd, randData, key)[:8]
        self.apdu = cmd  
        self.postProcess()
        
    def changePin(self,oldPin, newPin):
        if len(oldPin) % 2 != 0:
            oldPin += 'F'
        if len(newPin) % 2 != 0:
            newPin += 'F'
        cmd = '805E0100' + LV(oldPin + 'FF' + newPin)
        self.apdu = cmd  
        self.postProcess()
    def reloadPin(self,newPin, key):
        if len(newPin) % 2 != 0:
            newPin += 'F'
        key = Algo_Xor(key[:16],key[16:]) 
        cmd = '805E0000' + LV(newPin + Algo_MAC(newPin, '00' * 8, key)[:8])
        self.apdu = cmd 
        self.postProcess()
        
    def applicationUnblock(self,rand, key):
        cmd = '8418000004'
        cmd = cmd + Algo_MAC(cmd, rand, key)[:8]
        self.apdu = cmd 
        self.postProcess()
        
    def cardBlock(self,rand, key):
        cmd = '8416000004'
        cmd = cmd + Algo_MAC(cmd, rand, key)[:8]
        self.apdu = cmd
        self.postProcess()
         
    def externalAuthentication(self,index, rand, key):
        cmd = '008200' + index + LV(Algo_DES_Encryption_ECB(rand, key))
        self.apdu = cmd 
        self.postProcess()
        
    def internalAuthentication(self, data):
        cmd = '0088'+'0000' + LV(data)
        self.apdu = cmd           
        self.postProcess()
    def getAppletRandom(self,aidList):
        apdub = ''
        for e in aidList:
            apdub += LV(e)
        self.apdu = '80AA0600' + LV(apdub)
        self.postProcess()
    def appletBackUp(self,oldAID,newAID,schemeID,random,key):
        authData  =  Algo_DES_Encryption_ECB(random,key)
        apduB = 'E1' + LV(LV(oldAID) + LV(newAID) + LV(schemeID) + authData)
        self.apdu = '80AA0000' + LV(apduB)
        self.postProcess()
    def appletRestore(self,l):
        apduB = ''
        for e in l:
            apduB += LV(e[0] + e[1])
        self.apdu = '80AA0100' + LV(apduB)
        self.postProcess()
        
    def generateRSAKeyPair(self):
        self.res,self.sw = self.gp.Send('8045000000', self.card)
    def getLoadProof(self,random,aid):
        self.apdu = '80440000'+ LV(random + LV(aid))
        self.postProcess()

 
    def postProcess(self):
        self.ins = self.apdu[2:4]
        self.res = ''
        self.sw = ''
        self.res,self.sw = self.card.Transmit(self.apdu)
        self.sw1 = self.sw[:2]
        self.sw2 = self.sw[2:4]
        self.apduList.append(self.apdu)
        if(self.collectTime):
            self.timeList.append([self.ins,self.card.processTime])
        if self.checkSW:
            CheckIf(self.sw == '9000')
                
        
