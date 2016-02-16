from apptest import Card
from apptest.Card import CheckIf
from apptest.TLV import LV
import const, APDU 

from apptest.Algorithm import Algo_DES_Encryption_ECB, Algo_MAC, Algo_Xor

class Test():
    def __init__(self,card):
        pass

class Transaction(Test): 
    def __init__(self):
        pass
        
    def load(self,term,adf,apdu):
        apdu.selectAID(adf.aid)
        apdu.selectFID(adf.fid)
        pin  ='888888'
        apdu.verifyPin(pin)
        assert apdu.sw == '9000'

        apdu.initForLoad(term.tsType == const.TTI_EP_LOAD ,term.key.keyNo ,term.tsAmount , term.id )
        CheckIf(apdu.sw == '9000')
        # Check response 
        balance  = apdu.res[:8] 
        olCtr  = apdu.res[8:12] 
        #CheckIf(apdu.res[12:14] == term.key.)
        #CheckIf(apdu.res[14:16] == f. )
        rnd = apdu.res[16:24]
        sesk = Algo_DES_Encryption_ECB(rnd+olCtr+'8000',term.key.keyValue)
        CheckIf(apdu.res[24:] == Algo_MAC(balance + term.tsAmount + term.tsType + term.id, '00' * 8, sesk)[:8])
        # Genarate MAC2
        mac2 = Algo_MAC(term.tsAmount  +term.tsType + term.id + term.dateTime, '00' * 8, sesk)[:8]
        apdu.creditForLoad(term.dateTime , mac2)
        CheckIf(apdu.sw == '9000')

        
        
    def cappLoad(self,term,adf,apdu):
        pass
        
        
    def purchase(self,term,adf,apdu):
        apdu.selectAID(adf.aid)
        apdu.selectFID(adf.fid)
        apdu.initForPurchase(term.tsType == const.TTI_EP_PURCHASE,term.key.keyNo ,term.tsAmount , term.id )
        balance  = apdu.res[:8] 
        offCtr  = apdu.res[8:12]
        rand = apdu.res[-8:]
        # Generate SESK
        sesk = Algo_DES_Encryption_ECB(rand + offCtr + term.tsCtr[-4:], term.key.keyValue)
        mac1  = Algo_MAC(term.tsAmount + term.tsType + term.id + term.dateTime,'00' * 8,sesk)[:8]
        apdu.debitForPurchase(term.tsCtr,term.dateTime,mac1)
        assert apdu.sw == '9000'
        CheckIf(apdu.res[8:] == Algo_MAC(term.tsAmount , '00' * 8, sesk)[:8])

    
    def cappPurchase(self,term,adf,apdu):
        apdu.selectAID(adf.aid)
        keyf = adf.findEF('00')
        f = adf.findEF('02')
        
        pin = keyf.getKeyByType(const.KEY_TYPE_PIN)
        apdu.verifyPin(pin.keyValue)
        apdu.initializeForCappPurchase(term.key.keyNo ,term.tsAmount , term.id )
        CheckIf(apdu.res[:8] == f.balance)
        CheckIf(apdu.res[8:12] == f.offCtr)
        CheckIf(apdu.res[12:18] == adf.overDrawLimit)
        rand = apdu.res[-8:]
        
        # Update capp datacache 
        for k,v in term.capp.items():
            sfi =  k[:2]
            tag = k[2:4]
            apdu.updateCappDataCache(tag,sfi,v)
            assert apdu.sw == '9000'
            ef =  adf.findEF (sfi)
            ef.updateRecordByTag(v)
        
        # Generate SESK
        sesk = Algo_DES_Encryption_ECB(rand + f.offCtr + term.tsCtr[-4:], term.key.keyValue)
        mac1  = Algo_MAC(term.tsAmount + term.tsType + term.id + term.dateTime,'00' * 8,sesk)[:8]
        apdu.debitForPurchase(term.tsCtr,term.dateTime,mac1)
        assert apdu.sw == '9000'
        CheckIf(apdu.res[8:] == Algo_MAC(term.tsAmount , '00' * 8, sesk)[:8])
        tacKey = keyf.getKeyByType(const.KEY_TYPE_TAC)
        tacSesk = Algo_Xor(tacKey.keyValue[:16], tacKey.keyValue[16:])
        newBlc = '%08X' % (int(f.balance, 16) - int(term.tsAmount, 16))
        tac = Algo_MAC(term.tsAmount + term.tsType + term.id + term.tsCtr+ term.dateTime, '00' * 8, tacSesk)[:8]
        CheckIf(apdu.res[:8] == tac)
        mac2 = Algo_MAC(term.tsAmount, '00' * 8, sesk)[:8]
        CheckIf(apdu.res[8:] == mac2)
        
        f.balance = newBlc
        f.offCtr = '%04X'%(int(f.offCtr,16) + 1)
        adf.tsProve = {f.offCtr + term.tsType:mac2 + tac}
        adf.saveTransactionLog(term,f)
        
    def cashWithDraw(self,term,adf,apdu):
        apdu.selectAID(adf.aid)
        keyf = adf.findEF('00')
        f = adf.findEF('01')
        pin = keyf.getKeyByType(const.KEY_TYPE_PIN)
        apdu.verifyPin(pin.keyValue)
        apdu.initForPurchase(term.tsType == const.TTI_EP_PURCHASE,term.key.keyNo ,term.tsAmount , term.id )
        CheckIf(apdu.res[:8] == f.balance)
        CheckIf(apdu.res[8:12] == f.offCtr)
        CheckIf(apdu.res[12:18] == adf.overDrawLimit)
        rand = apdu.res[-8:]
        # Generate SESK
        sesk = Algo_DES_Encryption_ECB(rand + f.offCtr + term.tsCtr[-4:], term.key.keyValue)
        mac1  = Algo_MAC(term.tsAmount + term.tsType + term.id + term.dateTime,'00' * 8,sesk)[:8]
        apdu.debitForPurchase(term.tsCtr,term.dateTime,mac1)
        assert apdu.sw == '9000'
        CheckIf(apdu.res[8:] == Algo_MAC(term.tsAmount , '00' * 8, sesk)[:8])
        tacKey = keyf.getKeyByType(const.KEY_TYPE_TAC)
        sesk = Algo_Xor(tacKey.keyValue[:16], tacKey.keyValue[16:])
        newBlc = '%08X' % (int(f.balance, 16) - int(term.tsAmount, 16))
        tac = Algo_MAC(term.tsAmount + term.tsType + term.id + term.tsCtr+ term.dateTime, '00' * 8, sesk)[:8]
        CheckIf(apdu.res[:8] == tac)
        f.balance = newBlc
        f.offCtr = '%04X'%(int(f.offCtr,16) + 1)
        adf.saveTransactionLog(term,f)
            
    def readLoadLog(self,apdu):
        pass
        
    def getBalanceThenCheck(self,adf,apdu,type): 
        keyf = adf.findEF('00')
        pin = keyf.getKeyByType(const.KEY_TYPE_PIN)
        apdu.verifyPin(pin.keyValue)
        if type == 'EP':
            f = adf.findEF('02')
        else:
            f = adf.findEF('02')
        apdu.getBalance(type == 'EP')
        return apdu.res == f.balance
    
    def readCappDataThenCheck(self,apdu,capp):
        for k,v in capp.items():
            sfi =  k[:2]
            tag = k[2:4]
            apdu.readRecord(tag,sfi,'00',mode = 0)
            assert apdu.sw == '9000'
            assert apdu.res == v
            
            
  
            
