'''

'''
import Util, const  


class Terminal():
    def __init__(self):
        # variables 
        self.key = ''
        self.tsAmount = '00'*4
        self.tsType = const.TTI_ED_LOAD
        self.id  = '6100'+Util.generateRnd(4)
        self.dateTime = Util.getCurrentDateTime()  
        self.rnd = Util.generateRnd(8)
        self.tsCtr = '11223344'
        self.capp = {}
    def shift2AnotherCity(self):
        self.id = Util.generateRnd(6)
    def shift2Local(self):
        self.id  = '6100'+Util.generateRnd(4)
        