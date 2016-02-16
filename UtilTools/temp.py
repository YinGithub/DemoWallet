''''l = ('WALLET.01','WALLET.02','WALLET.03','WALLET.04','WALLET.05','WALLET.06','WALLET.07','WALLET.08','WALLET.09','WALLET.10')
l_a = []
for e in l:
    l_a.append(e.encode('hex'))
    
print l_a 
import re
s = '(((KEY_INDEX)(TS_AMT)(WE))112233445566)'
# merchanism

p = re.compile('\(\w.*?\)')
s1 = p.findall(s)
print s1'''
from apptest.Algorithm import Algo_DES_Encryption_ECB, Algo_MAC
l = ['57414c4c45542e3031', '57414c4c45542e3032', '57414c4c45542e3033', '57414c4c45542e3034', '57414c4c45542e3035', '57414c4c45542e3036', '57414c4c45542e3037', '57414c4c45542e3038', '57414c4c45542e3039', '57414c4c45542e3130']
'''
from json.encoder import JSONEncoder
class Parser():
    def __init__(self,rawFileName):
        self.dCmdFlow = {}
        self.fn = rawFileName
        self._parse()
        self._output()
        
    def _parse(self):
        cmdList  = []
        self.dCmdFlow['KeyBase'] = cmdList
        rawList = self._input()
        i = 1
        for e in rawList :
            d  = {}
            if i <= 5:
                d['type'] = 'purchase'
                d['key_index'] = '%02X'%i
                d['key_value'] = e 
            else:
                d['type'] = 'load'
                d['key_index'] = '%02X'%(i-5)
                d['key_value'] = e 
                       
            cmdList.append(d)
            i = i+1
    
    
    def _input(self):
        f = open('keyBase','r')
        l = f.readlines()
        f.close()
        return [e.replace('\n','') for e in l]
            
    def _output(self):
        f = open(self.fn+'.json','w')
        f.seek(0)
        s = JSONEncoder().encode( self.dCmdFlow)
        f.write(s)
        f.close()
        '''
        #sesk = Algo_DES_Encryption_ECB(rand + offCtr + term.tsCtr[-4:], term.key.keyValue)
        #mac1  = Algo_MAC(term.tsAmount + term.tsType + term.id + term.dateTime,'00' * 8,sesk)[:8]
k = '0BA5B6D33FEC6DD73A5AA6CF81E818C7'
rnd  = '110F960F'
ctr = '0013'


sesk = Algo_DES_Encryption_ECB(rnd+ctr+'3344',k)
mac  = Algo_MAC('0000FFED0611223344556620160115162449677','00' * 8,sesk)[:8]
print sesk
print mac
#mac2 = Algo_MAC('8877665544332211', '00' * 8, '11223344556677881122334455667700')






        