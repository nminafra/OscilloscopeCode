import socket
import threading
import sys
import time
import string
from select import select
import Queue



class myClient(threading.Thread):

    def __init__(self): 
        super(myClient, self).__init__()
        self.connected = threading.Event()
        self.alive = threading.Event()
        self.connectionLock = threading.Lock()
        self.alive.set()
        self.TCPQueue = Queue.Queue(10)

    def connect(self,tcpIP):
    
        self.connectionLock.acquire()
        
        if self.connected.isSet():
            print "device already connected"
        else:
            try:
                print "Connecting to device..."
                self.TCPSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.TCPSock.connect(tcpIP)           
                self.connected.set()
                self.interfaces = [self.TCPSock]       # [self.UDPSock,self.TCPSock]
         
                #cmd = "*idn?" + "\n"
                #cmd = ":acquire:mode?" + "\n"
                #cmd = ":channel1:display on" + "\n"
                #self.TCPSock.send(cmd) 
                #self.deviceID = self.receive()
                #sys.stdout.write("Connected to device: "+self.deviceID+"\n")
                
            except socket.error as e:
                sys.stderr.write("Device connection error:"+str(e)+"\n")        
        self.connectionLock.release()
        
        
    def disconnect(self):
        self.connectionLock.acquire()
        if self.connected.isSet():
            try:
                self.TCPSock.shutdown(1)
                self.TCPSock.close()
                self.connected.clear()
                sys.stdout.write("Disconnected from device."+"\n")
            except socket.error as e:
                sys.stderr.write("Device disconnection error:"+str(e)+"\n")
        else:
            sys.stderr.write("WARNING: nothing to disconnect\n")
        self.connectionLock.release()
        
        
    def run(self):        
        while self.alive.isSet():
            self.connectionLock.acquire()
            if self.connected.isSet():
                self.TCPMessage=self.receive()
                if self.TCPMessage!="None":
                    try:
                        self.TCPQueue.put(self.TCPMessage)
                    except Queue.Full as e:      
                        sys.stdout.write ("TCP queue full")
                    #sys.stdout.write("Receiving form TCP: "+str(self.TCPMessage)+"\n")
            else:
                time.sleep(0.1)
            self.connectionLock.release()
    
   
    def receive(self):
        inputReady,outputReady,exceptReady = select(self.interfaces,[],[],1)  #wait for data in interfaces list
        for s in inputReady:              
            if s == self.TCPSock:        
                self.buffer = self.readTCP(2048)
                return self.buffer
            else:
                sys.stderr.write("UNKNOWN SOCKET TYPE")
                return "TCP error"
        return "None"
        
    def sendTCP(self,message):
        if self.connected.isSet():
            self.TCPSock.send(message)
        else:
            sys.stderr.write("No device connected!\n")
        
    def readTCP(self,nByte = 20, peek = False):
        data,ip = self.TCPSock.recvfrom(nByte,peek * socket.MSG_PEEK)
        return data
    
    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)
