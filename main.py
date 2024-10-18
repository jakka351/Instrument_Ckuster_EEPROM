#!/usr/bin/python3
#coding:utf-8
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#region Copyright (c) 2024, Jack Leighton
#     __________________________________________________________________________________________________________________
#
#                  __                   __              __________                                      __   
#                _/  |_  ____   _______/  |_  __________\______   \_______   ____   ______ ____   _____/  |_ 
#                \   __\/ __ \ /  ___/\   __\/ __ \_  __ \     ___/\_  __ \_/ __ \ /  ___// __ \ /    \   __\
#                 |  | \  ___/ \___ \  |  | \  ___/|  | \/    |     |  | \/\  ___/ \___ \\  ___/|   |  \  |  
#                 |__|  \___  >____  > |__|  \___  >__|  |____|     |__|    \___  >____  >\___  >___|  /__|  
#                           \/     \/            \/                             \/     \/     \/     \/      
#                                                          .__       .__  .__          __                    
#                               ____________   ____   ____ |__|____  |  | |__| _______/  |_                  
#                              /  ___/\____ \_/ __ \_/ ___\|  \__  \ |  | |  |/  ___/\   __\                 
#                              \___ \ |  |_> >  ___/\  \___|  |/ __ \|  |_|  |\___ \  |  |                   
#                             /____  >|   __/ \___  >\___  >__(____  /____/__/____  > |__|                   
#                                  \/ |__|        \/     \/        \/             \/                         
#                                  __                         __  .__                                        
#                   _____   __ ___/  |_  ____   _____   _____/  |_|__|__  __ ____                            
#                   \__  \ |  |  \   __\/  _ \ /     \ /  _ \   __\  \  \/ // __ \                           
#                    / __ \|  |  /|  | (  <_> )  Y Y  (  <_> )  | |  |\   /\  ___/                           
#                   (____  /____/ |__|  \____/|__|_|  /\____/|__| |__| \_/  \___  >                          
#                        \/                         \/                          \/                           
#                                                  .__          __  .__                                      
#                                       __________ |  |  __ ___/  |_|__| ____   ____   ______                
#                                      /  ___/  _ \|  | |  |  \   __\  |/  _ \ /    \ /  ___/                
#                                      \___ (  <_> )  |_|  |  /|  | |  (  <_> )   |  \\___ \                 
#                                     /____  >____/|____/____/ |__| |__|\____/|___|  /____  >                
#                                          \/                                      \/     \/                 
#                                   Tester Present Specialist Automotive Solutions
#     __________________________________________________________________________________________________________________
#      |--------------------------------------------------------------------------------------------------------------|
#      |       https://github.com/jakka351/| https://testerPresent.com.au | https://facebook.com/testerPresent        |
#      |--------------------------------------------------------------------------------------------------------------|
#      | Copyright (c) 2022/2023/2024 Benjamin Jack Leighton                                                          |          
#      | All rights reserved.                                                                                         |
#      |--------------------------------------------------------------------------------------------------------------|
#        Redistribution and use in source and binary forms, with or without modification, are permitted provided that
#        the following conditions are met:
#        1.    With the express written consent of the copyright holder.
#        2.    Redistributions of source code must retain the above copyright notice, this
#              list of conditions and the following disclaimer.
#        3.    Redistributions in binary form must reproduce the above copyright notice, this
#              list of conditions and the following disclaimer in the documentation and/or other
#              materials provided with the distribution.
#        4.    Neither the name of the organization nor the names of its contributors may be used to
#              endorse or promote products derived from this software without specific prior written permission.
#      _________________________________________________________________________________________________________________
#      THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#      INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#      DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#      SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#      SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#      WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
#      USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#      _________________________________________________________________________________________________________________
#
#       This software can only be distributed with my written permission. It is for my own educational purposes and  
#       is potentially dangerous to ECU health and safety. Gracias a Gato Blancoford desde las alturas del mar de chelle.                                                        
#      _________________________________________________________________________________________________________________
#
#
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#endregion License
#############################################################################################################
# library imports
#############################################################################################################
import os, sys, time, queue, traceback
from threading import *
from threading import Thread
from array import array
import can 
#################################################################################################################
# GNU/Linux socketcan canbus interfaces //
# // vcan0 is virtual socket for testing on linux socketcan
# // virtualcan is https://github.com/windelbouwman/virtualcan cross platform
#################################################################################################################
businput     = 'socketcan'
channelinput = 'vcan0'
bitrateinput = '125000'
MidSpeedCan  = can.interface.Bus(channel=channelinput, bustype=businput, bitrate=bitrateinput) # MS CAN
# // insert secret key here
fixed                                                 = 0xbfa49056cd 
# // ecu rx can id insert here
DiagSix_Rx                                            = 0x728
DiagSig_Tx                                            = DiagSig_Rx + 0x08
ServiceRequest                                        = dict()
#################################################################################################################
# EEPROM PROCESS
#################################################################################################################
def msgbuffer():
    global message, q,DiagSig_Rx                                      
    while True:
        message = MidSpeedCan.recv()          # if recieving can frames then put these can arb id's into a queue
        if message.arbitration_id == DiagSig_Rx:                        
            q.put(message)
        elif message.arbitration_id == DiagSig_Tx
            q.put(message)
'''
#################################################################################################################
# EEPROM PROCESS
#################################################################################################################
Jack Whiteford
“FG(I) Read and Write the entire EEPROM:
########################################
### < send to Cluster
### > Cluster responds
    03 22 E2 00 <                Request data by ID
    06 62 E2 00 17 0B 6C >       Data is 170B6C - might be checking model?
    02 BA 0B <         Quickly jam in these two..
    02 BA 07 <      ..requests that "fail" (you will get en error)
    FA 11 88 57 >   3 byte challenge key appears out of nowhere
                    (If it doesn't appear, try again from BA0B)
    04 BA 8E 5C 8D < Respond with 3 byte key generated with { 0xbf, 0xa4, 0x90, 0x56, 0xcd }
    02 10 FA <       Don't wait, just do
    02 50 FA >       Success!
    BA 01 02 00 00 < Read 2 bytes at EEPROM address 0x0000
    FA 01 02 15 A1 > !!! 0xA1 is byte 0, 0x15 is byte 1 in the EEPROM.
    BA 02 02 00 00 16 A1 < !!! Write 2 bytes at address 0x0000
                        !!! 16 was 15 increased by 1 as a test
    FA 02 02 > Happy days
                    (FYI)
    BA 01 02 00 02 < Read 2 bytes at address 0x0002, next two bytes
                        ...and on it goes...
    BA 01 02 01 FE < Read 2 bytes at address 0x01FE the last EEPROM address
                     (I say last, but I also assume the 02 means two byte read/write)
                     (You probably/might be able to read and write 1 byte at a time)
    02 10 81 < Request to leave secure mode
    02 50 81 > Left secure mode
    02 11 01 < reset
    02 51 01 > yeah yeah”
############################################
Please forward onto Jakka - I expect him to come up with a neat script to do all the things I did for the FGII”
“Thoughts: It's probably worth doing a reset also at the end of any EEPROM write, to make sure any cached data in RAM isn't kept.//
##################################################################################################################

'''
#############################################################################################################
# function that generates the key
#############################################################################################################
def KeyGen(seed, fixed):
    seed   = requestSecurityAccess(DiagSix_Rx, 0x01)
    try: 
        challengeCode = array('Q')
        challengeCode.append(fixed & 0xff)
        challengeCode.append((fixed >> 8) & 0xff)
        challengeCode.append((fixed >> 16) & 0xff)
        challengeCode.append((fixed >> 24) & 0xff)
        challengeCode.append((fixed >> 32) & 0xff)
        challengeCode.append(seed[2])
        challengeCode.append(seed[1])
        challengeCode.append(seed[0])
        temp1 = 0xC541A9
        for i in range(64):
            abit = temp1 & 0x01
            chbit = challengeCode[7] & 0x01
            bbit = abit ^ chbit
            temp2 = (temp1 >> 1) + bbit * 0x800000 & -1
            temp1 = (temp2 ^ 0x109028 * bbit) & -1
            challengeCode[7] = challengeCode[7] >> 1 & 0xff
            for a in range(7, 0, -1):
                challengeCode[a] = challengeCode[a] + (challengeCode[a - 1] & 1) * 128 & 0xff
                challengeCode[a - 1] = challengeCode[a - 1] >> 1
        key = [ temp1 >> 4 & 0xff, ((temp1 >> 12 & 0x0f) << 4) + (temp1 >> 20 & 0x0f), (temp1 >> 16 & 0x0f) + ((temp1 & 0x0f) << 4) ]
        print("Succesfully got key: {key}")
        return key
    except can.CanError():
        print("CAN Error")            
#############################################################################################################
# function to send key 
# Usage: SendKey(key) should be all that needs to be called.
#############################################################################################################
def SendKey(key):
    keyResponse   = can.Message(arbitration_id = DiagSig_Rx,
                                 data          = [0x04, 0xBA, key[0], key[1], key[2], 0, 0, 0], is_extended_id = False)
    MidSpeedCan.Send(keyResponse)
#############################################################################################################
# MAIN
#
############################################################################################################
def main:
    glboal message, MidSpeedCan, q, fixed, DiagSig_Rx, DiagSig_Tx
     try:
        while True:
            for i in range(8):
                while(q.empty() == True):                               # wait for messages to queue
                    pass
                message = q.get()   
                c = '{0:f},{1:d},'.format(message.timestamp,count)
                requestDataById = can.Message(arbitration_id=DiagSig_Rx, data=[0x03, 0x22, 0x62, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
                MidSpeedCan.Send(requestDataById)
                ba0b = can.Message(arbitration_id=DiagSig_Rx, data=[0x02, 0xBA, 0x0B, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
                MidSpeedCan.Send(ba0b)
                ba07 = can.Message(arbitration_id=DiagSig_Rx, data=[0x02, 0xBA, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
                MidSpeedCan.Send(ba07)
                if message.arbitration_id == DiagSig_Rx:
                    print(message)
                elif message.arbitration_id == DiagSig_Tx:
                    print(message)
                elif message.arbitration_id == DiagSig_Tx and  and message.data[0] == 0xFA:
                    print("Got Seed: ", message.data[1], message.data[2], message.data[3])
                    seed    = message.data[1], message.data[2], message.data[3]
                    seed[0] = message.data[1]
                    seed[1] = message.data[2]
                    seed[2] = message.data[3]
                    print("Generating Key...")
                    Keygen(seed, fixed)
                    SendKey(key)
                    systemSupplierSpecific = can.Message(arbitration_id=DiagSig_Rx, data=[0x02, 0x10, 0xFA, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
                    MidSpeedCan.Send(systemSupplierSpecific)
                    data = 0x00
                    print("EEPROM: ")
                    for address in range(0x0000, 0x01FF, 2):
                        address_high = (address >> 8) & 0xFF
                        address_low = address & 0xFF
                        read_eeprom = can.Message(arbitration_id=DiagSig_Rx, data=[0x05, 0xBA, 0x01, 0x02, address_high, address_low, 0x00, 0x00 ],extended_id=False)
                        eeprom = MidSpeedCan.recv()
                        if eeprom.arbitration_id == DiagSig_Tx: & eeprom.data[2] == 0xFA:
                            data += eeprom.data[4], eeprom.data[5]
                            print(data)
                        if address == 0x1FF:
                            break                                                     
    except KeyboardInterrupt:
        sys.exit(0)                                              # quit if ctl + c is hit
    except Exception:
        traceback.print_exc(file=sys.stdout)                     # quit if there is a python problem
        sys.exit()
    except OSError:
        sys.exit()                                               # quit if there is a system issue  

#################################################################################################################
if __name__ == "__main__":
    q                      = queue.Queue()                       #
    rx                     = Thread(target = msgbuffer)          #
    rx.start()                                                   # start the rx thread and queue msgs
    main()                                                       # match ca
