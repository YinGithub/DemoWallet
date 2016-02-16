from json.decoder import JSONDecoder
import re
from apptest import Card
from lib import Util, const
from lib.APDU import APDU
from apptest.Algorithm import Algo_DES_Encryption_ECB, Algo_MAC
def _CalcMac(type,res):
        if type == 'load':
            balance  = res[:8] 
            olCtr  = res[8:12] 
            rnd = res[16:24]
            sesk = Algo_DES_Encryption_ECB(rnd+olCtr+'8000',d['LOAD_KEY'])
            assert(res[24:] == Algo_MAC(balance + d['TS_AMT'] + const.TTI_EP_LOAD + '112233445566', '00' * 8, sesk)[:8])
            # Genarate MAC2
            mac2 = Algo_MAC(d['TS_AMT']  +const.TTI_EP_LOAD + '112233445566' + d['DATE'], '00' * 8, sesk)[:8]
            return mac2 
            
d = {'AID':'57414c4c45542e3031','KEY_INDEX':'01','TS_AMT':'00000001','DATE':'20160111210330','LOAD_KEY':'42EAF305CDE83EC62C67BCB44B946B65'}
def _loadScript(fn):
    try:
        fp = open(fn,'r')
    except:
        fp.close()
        return
    s = fp.readline()
    s.replace('\n','')
    d = JSONDecoder().decode(s)
    return [(e['checker'],e['command']) for e in d['commandsFlow'] ]
    
def _parseAndRun(sList):
    card = Card.Card()
    apdu = APDU(card)
    import  re 
    apduList  = []
    for e in sList:
        cmd = e[1]
        p1 = re.compile('\(\w.*?\)')
        brckList  = p1.findall(cmd)
        for f in brckList:
            if d.has_key(f[1:-1]):
                cmd  = cmd.replace(f,d[f[1:-1]])
            elif f[1:-1] == 'MAC':
                if '8052' in cmd:
                    mac  = _CalcMac(type= 'load',res = apdu.res)
                else:
                    mac = _CalcMac(type= 'purchase',res = apdu.res)
                cmd= cmd.replace(f,mac)
                    
            else:    
                print f
                assert 0,'Unknow ELement!'
        p = re.compile('\(.*\)')
        brckList = p.findall(cmd)
        if len(brckList)> 0:
            cmd = cmd.replace(brckList[0],brckList[0][1:-1])
        if '#' in  cmd:
            cmd = cmd.replace('#','%02X'%(len(cmd[cmd.index('#'):])/2))
        apduList.append(cmd)
        apdu.send(cmd)
        assert apdu.sw == '9000'
        
def run(fn):
    sList = _loadScript(fn)
    apduList = _parseAndRun(sList)
    print apduList
if __name__ == '__main__':
    run('LoadScript.json')
    pass