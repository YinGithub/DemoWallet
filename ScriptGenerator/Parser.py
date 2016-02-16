from json.encoder import JSONEncoder
class Parser():
    def __init__(self,rawFileName):
        self.dCmdFlow = {}
        self.fn = rawFileName
        self._parse()
        self._output()
        
    def _parse(self):
        cmdList  = []
        self.dCmdFlow['commandsFlow'] = cmdList
        rawList = self._input()
        i = 0
        for e in rawList :
            i = i+1
            d  = {}
            d['index'] = '%d'%i
            l = e.split(' ')
            d['command'] = l[0]
            print l
            d['checker'] = '.*'+l[1]+'$'
            if len(l) > 2:
                d['dis'] = l[2]
            cmdList.append(d)
    
    
    def _input(self):
        try:
            f  = open(self.fn,'r')
        except:
            f.close()
            return
        else:
            l = f.readlines()
            f.close()
            return [e.replace('\n','') for e in l]
            
    def _output(self):
        f = open(self.fn+'.json','w')
        f.seek(0)
        s = JSONEncoder().encode( self.dCmdFlow)
        f.write(s)
        f.close()
        


if __name__ == '__main__':
    
    Parser('ClearCard')
    print 'ok'
    
        