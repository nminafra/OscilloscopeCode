#!/usr/bin/env python

import sys
import time
from myClient import *

#MAIN
if __name__ == "__main__":  

    print "Starting test application"
    print "Starting socket thread...."
 
    ####################################################################
    # init sequence (opens connection to server and check device)
    ####################################################################   
    #gives the IP addres of the osciloscope
    tcpIP   = "127.0.0.1"
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
    print TCPFromQueue

    # TO BE ADDED RESET SCOPE + LOAD CONFIGURATION
    a=0;
    while a<100:
      ####################################################################
      # start DAQ and check until the DAQ loop is done
      ####################################################################
      #run command for the DAQ
      print "starting the DAQ: \n"
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

      
      ####################################################################
      # Store the DAQ 
      ####################################################################
      print "\n storing data:ch1"
      
    
      myClient.sendTCP("*CLS\n")
      teststring=":disk:save:waveform channel1,\"C:\\TEMP\\test%d.bin\",bin,off" %a
      #print teststring		
      myClient.sendTCP(":disk:save:waveform channel1,\"D:\\TEMP\\testch1_%d.bin\",bin\n" %a)
  


      myClient.sendTCP("*OPC\n")
      time.sleep(0.1)
      TCPFromQueue="-1"
      myClient.sendTCP("*ESR?\n");
      while TCPFromQueue<>"+1\n":
        #myClient.sendTCP("*ESR?\n")
        try:
          TCPFromQueue=myClient.TCPQueue.get(True,0.1)
          #print TCPFromQueue
        except Queue.Empty as e:
          sys.stdout.write(str('.'))
        #print TCPFromQueue  
        time.sleep(1)
      
     # print "\n storing data:ch2"  
      #myClient.sendTCP(":disk:save:waveform channel2,%s%sch2_%d.bin\",bin,on\n" %"\"C:\\TEMP\\","test",a,)
 #     myClient.sendTCP(":disk:save:waveform channel2,\"C:\\TEMP\\testch2_%d.bin\",bin\n" %a)
 #    
 #     myClient.sendTCP("*OPC\n")
 #     time.sleep(0.1)
 #     TCPFromQueue="-1"
 #     myClient.sendTCP("*ESR?\n");
 #     while TCPFromQueue<>"+1\n":
 #       #myClient.sendTCP("*ESR?\n")
 #       try:
 #         TCPFromQueue=myClient.TCPQueue.get(True,0.1)
 #         #print TCPFromQueue
 #       except Queue.Empty as e:
 #         sys.stdout.write(str('.'))
 #       print TCPFromQueue  
 #       time.sleep(1)

      print "\n storing data:ch3"  
      myClient.sendTCP(":disk:save:waveform channel3,\"D:\\TEMP\\testch3_%d.bin\",bin\n" %a)
      myClient.sendTCP("*OPC\n")
      time.sleep(0.1)
      TCPFromQueue="-1"
      myClient.sendTCP("*ESR?\n");
      while TCPFromQueue<>"+1\n":
        #myClient.sendTCP("*ESR?\n")
        try:
          TCPFromQueue=myClient.TCPQueue.get(True,0.1)
          #print TCPFromQueue
        except Queue.Empty as e:
          sys.stdout.write(str('.'))
        #print TCPFromQueue  
        time.sleep(1)
        
 #     print "\n storing data:ch4"  
 #     myClient.sendTCP(":disk:save:waveform channel4,\"C:\\TEMP\\testch4_%d.bin\",bin\n" %a)
 #     myClient.sendTCP("*OPC\n")
 #     time.sleep(0.1)
 #     TCPFromQueue="-1"
 #     myClient.sendTCP("*ESR?\n");
 #     while TCPFromQueue<>"+1\n":
 #       #myClient.sendTCP("*ESR?\n")
 #       try:
 #         TCPFromQueue=myClient.TCPQueue.get(True,0.1)
 #         #print TCPFromQueue
 #       except Queue.Empty as e:
 #         sys.stdout.write(str('.'))
 #       print TCPFromQueue  
 #       time.sleep(1)
 #
      ####################################################################
      # do we want to start again? 
      ####################################################################
      a=a+1;


 #   while 1:
 #     #myClient.sendTCP("*ESR?\n")
 #     TCPFromQueue="X"
 #     try:
 #       TCPFromQueue=myClient.TCPQueue.get(True,0.1)
 #       print "stil in Q %s \n" %TCPFromQueue
 #       #print TCPFromQueue
 #     except Queue.Empty as e:
 #       sys.stdout.write(str('.'))
 #     time.sleep(100)
    
    
    ####################################################################
    # Stop the DAQ
    ####################################################################
    print "\n Disconnecting...."
    myClient.disconnect()
    print "Still disconnecting" 
    myClient.join()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    