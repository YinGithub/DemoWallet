import random
from apptest import GP
import time
testAppletAid = 'A000000003'
def installTestApplet(card):
    gp = GP.GP()
    gp.Authentication(card, '01')
    gp.Delete(testAppletAid, card)
    gp.Install('A000000001', 'A000000003', testAppletAid , card) #card lock



def generateRnd(len):
    return  ''.join(['%02X'%random.randint(0,0xFF)for i in range(0,len)])
def generateDecimalRnd(len):
    return  ''.join(['%02d'%random.randint(0,99)for i in range(0,len)])
def getCurrentDateTime():
    return time.strftime("%Y%m%d%H%M%S")
