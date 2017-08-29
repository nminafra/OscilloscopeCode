#!/usr/bin/env python

import sys
import time
import serial
import time
import os

from myClient import *
ser = serial.Serial('COM3', 9600, timeout=0)
#was com3
myClient
#file_path="D:\\DESY_03Feb\\"
#file_name="Config8"
Segments=1000 


def capture_data():
    #run command for the DAQ
    print "\n starting the DAQ: \n"
    myClient.sendTCP("*CLS\n")
    myClient.sendTCP(":run\n")
    if myClient.TCPQueue.empty==False:
      print "shit que is not empty"
      #ader query receives ''+1'' when the DAQ finishes.
      #this bit is reset once read
    TCPFromQueue='-1' 
    while TCPFromQueue!='+1\n':
      myClient.sendTCP(":ader?\n")#idn?
      try:
        TCPFromQueue=myClient.TCPQueue.get(True,0.1)
      except Queue.Empty as e:
        sys.stdout.write(str(e))
      sys.stdout.write(str('.'))
      time.sleep(1)

def save_channel(channel_number, file_number):
    print ("\n storing data:ch%d,%s%s_file_%d_CH%d.bin") %(channel_number,file_path,file_name,file_number,channel_number)
    myClient.sendTCP("*CLS\n")

    myClient.sendTCP(":disk:save:waveform channel%d,\"%s%s_file_%d_CH%d.bin\",bin\n" %(channel_number,file_path,file_name,file_number,channel_number))
  
    myClient.sendTCP("*OPC\n")
    time.sleep(0.1)
    TCPFromQueue="-1"
    myClient.sendTCP("*ESR?\n");

    #wait util response
    while TCPFromQueue<>"+1\n":
      #myClient.sendTCP("*ESR?\n")
      try:
        TCPFromQueue=myClient.TCPQueue.get(True,0.1)
      #print TCPFromQueue
      except Queue.Empty as e:
        sys.stdout.write(str('.'))
      #print TCPFromQueue  
      time.sleep(1)


#MAIN
if __name__ == "__main__":


    

    if len(sys.argv)<4:
        print ("\n***********DAQv2.0 usage*********")
        print ("1.destination folder")
        print ("2.file base name")
        print ("3.number of segmented acquisition\n\n")
        exit()


    print "Starting test application"
    print "Starting socket thread...."
 

    file_path=sys.argv[1]
    file_name=sys.argv[2]
    fileMax=int(sys.argv[3])
    #################################################################
    valueVboosterMIN=2.3 #2.3
    valueVboosterMAX=2.7 #2.8
    
    valueVPreampMIN=1.8 #2.0
    valueVPreampMAX=2.4
    stepV=0.1
    stepVbooster=0.1
    ##################################################################

    ####################################################################
    # init sequence (opens connection to server and check device)
    ####################################################################   
    #gives the IP addres of the osciloscope
    tcpIP   = "127.0.0.1"
    #tcpIP   = "128.141.149.1"
    tcpPort = 5025

    #opens connection to the osciloscope
    myClient = myClient()
    myClient.start()    
    print "connecting to: %s: %d \n" % (tcpIP, tcpPort)
    myClient.connect((tcpIP,tcpPort))

    #read identification of the device
    myClient.sendTCP("*IDN?\n")
    time.sleep(0.1)
    TCPFromQueue=myClient.TCPQueue.get(True,0.1)
    print ("connected to device %s") %TCPFromQueue

            
    valueVbooster=valueVboosterMIN
    valueVpreamp=valueVPreampMIN

    file_path0 = file_path
            
    while((valueVbooster>=valueVboosterMIN)and(valueVbooster<=valueVboosterMAX)):
          valueVpreamp=valueVPreampMIN
          while((valueVpreamp>=valueVPreampMIN)and(valueVpreamp<=valueVPreampMAX)):
                
              

                print ("%d files called %s will be (hopefully) saved to %s\n") %(fileMax,file_name,file_path)

                commandSetVboost='V2 '+ str(valueVbooster) +'\n'
                commandSetVpreamp='V1 '+ str(valueVpreamp) +'\n'
         
                #var = bytearray('V2 1.153\n','ascii')
                var = bytearray(commandSetVboost,'ascii')
                ser.write(var)
                var = bytearray(commandSetVpreamp,'ascii')
                ser.write(var)
                var = bytearray('OP1 1\n','ascii')
                ser.write(var)
                var = bytearray('OP2 1\n','ascii')
                ser.write(var)

                var = bytearray('V2?\n','ascii')
                ser.write(var)
                var = bytearray('V1?\n','ascii')
                ser.write(var)

                newdir='LVSCAN_Preamp'+str(valueVpreamp)+'_Boost'+str(valueVbooster)
                file_path=file_path0+newdir
                print('Creating new directory:',file_path) 
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                file_path+= '\\'

                #selecting all segment
                myClient.sendTCP(":DISK:SEGMented ALL\n")

                # TO BE ADDED RESET SCOPE + LOAD CONFIGURATION
                fileIdx=0
                StartTime = time.time()
                while fileIdx<fileMax:
                    ####################################################################
                    # start DAQ and check until the DAQ loop is done
                    ####################################################################
                    capture_data()

                    ####################################################################
                    # Store the DAQ 

                    ####################################################################

                    StartTimeSaving = time.time()

                    save_channel(1,fileIdx)
                    #save_channel(2,fileIdx)
                    #save_channel(3,fileIdx)
                    #save_channel(4,fileIdx)

                    print "\nTime to save file number %d: %.2f\n" %  (fileIdx, time.time() - StartTimeSaving)
                    AverageFreq = Segments*(fileIdx+1)/(time.time() - StartTime)
                    print "Average (if %d segments: %.2f Hz\t\t%.2f events per hour" % (Segments,AverageFreq,AverageFreq*3600)

                    ####################################################################
                    # do we want to start again? 
                    ####################################################################
                    fileIdx=fileIdx+1;
                
                valueVpreamp=valueVpreamp+stepV
                
          valueVbooster=valueVbooster+stepVbooster



    ####################################################################
    # Stop the DAQ
    ####################################################################            
    print "\n Disconnecting...."
    myClient.disconnect()
    print "Still disconnecting" 
    myClient.join()
        
    
    
    
    
    
    
    
    
    
