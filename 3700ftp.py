import socket
import sys
import os

def parseUrl(url):
    # parses urls of the format ftp://[USER[:PASSWORD]@]HOST[:PORT]/PATH
    #ftp://barkermil:aqdZUKFMz96NlgWPQHSA@networks-teaching-ftp.ccs.neu.edu:21/
    
    param = url[6:]
    #first check for username/password
    temptuple = param.partition('@')
    plc = 0
    paramlist = [''] * 5
    if (temptuple[1] == '@'):
        param = temptuple[2]
        temptuple = temptuple[0].partition(':')
        #adding a beginning code so I can tell which things are included later
        paramlist[plc] = "us:" + ((str)(temptuple[0]))
        plc += 1
        paramlist[plc] = "ps:" + ((str)(temptuple[2]))
        plc += 1
    else:
        #then check for port
        param = temptuple[0]
    temptuple = param.partition(':')
    if (temptuple[1] == ':'):
        paramlist[plc] = "ho:" + ((str)(temptuple[0]))
        plc += 1
        temptuple = temptuple[2].partition('/')
        paramlist[plc] = "po:" + ((str)(temptuple[0]))
        plc += 1
        paramlist[plc] = "pt:/" + ((str)(temptuple[2]))
    else:
        temptuple = temptuple[0].partition('/')
        paramlist[plc] = "ho:" + ((str)(temptuple[0]))
        plc += 1
        paramlist[plc] = "pt:/" + ((str)(temptuple[2]))
    print(paramlist)
    return paramlist

#receives a message from socket s, and returns with said message
def receive(s):
    receiving = True
    inMessage = ""
    while(receiving):
        inMessage += str(s.recv(1024), "utf-8")
        if(inMessage.endswith('\r\n')):
            receiving = False
    return inMessage

def openData(s):
    outMessage = "PASV\r\n"
    s.sendall(bytes(outMessage, "utf-8"))
    inMessage = receive(s)
    print(inMessage)
    if(inMessage[:3] != "227"):
        print("Unsuccessful in opening data channel")
    justNums = (inMessage.partition("("))[2]
    numList = justNums.split(",")
    ip = numList[0] + "." + numList[1] + "." + numList[2] + "." + numList[3]
    dataPort = (((int)(numList[4])) << 8) + ((int)((numList[5])[:-4]))
    dataS = socket.socket()
    dataS.connect((ip, dataPort))
    return dataS

#Parse the command and inputs
syslen = len(sys.argv)
assert (sys.argv[0] == "./3700ftp"), "Invalid command"
if (syslen == 3):
    command = sys.argv[1]
    param1 = sys.argv[2]
elif(syslen == 4):
    command = sys.argv[1]
    param1 = sys.argv[2]
    param2 = sys.argv[3]
else:
    print("neither arg was a url")

if (param1[:6] == "ftp://"):
    paramlist = parseUrl(param1)
    firstParam = True
else:
    assert(param2[:6] == 'ftp://'), "Invalid input"
    paramlist = parseUrl(param2)
    firstParam = False

#Set the parameters
username = "anonymous"
password = ""
port = 21

for x in paramlist:
    if(x[:3] == "us:"):
        username = x[3:]
    if(x[:3] == "ps:"):
        password = x[3:]
    if(x[:3] == "ho:"):
        host = x[3:]
    if(x[:3] == "po:"):
        port = x[3:]
    if(x[:3] == "pt:"):
        path = x[3:]

#set up the control connection

controlS = socket.socket()
print("port: " + (str)(port))
controlS.connect((host, (int)(port)))

print(receive(controlS))

outMessage = "USER " + username + "\r\n"
controlS.sendall(bytes(outMessage, "utf-8"))
inMessage = receive(controlS)
print(inMessage)
if(inMessage[:3] != "230"):
    outMessage = "PASS " + password + "\r\n"
    controlS.sendall(bytes(outMessage, "utf-8"))
    print(receive(controlS))
outMessage = "TYPE I\r\n"
controlS.sendall(bytes(outMessage, "utf-8"))
print(receive(controlS))
outMessage = "MODE S\r\n"
controlS.sendall(bytes(outMessage, "utf-8"))
print(receive(controlS))
outMessage = "STRU F\r\n"
controlS.sendall(bytes(outMessage, "utf-8"))
print(receive(controlS))

#run the commands
if(command == "mkdir"):
    outMessage = "MKD " + path + "\r\n"
    controlS.sendall(bytes(outMessage, "utf-8"))
    print(receive(controlS))

if(command == "rmdir"):
    outMessage = "RMD " + path + "\r\n"
    controlS.sendall(bytes(outMessage, "utf-8"))
    print(receive(controlS))

if(command == "ls"):
    dataS = openData(controlS)
    outMessage = "LIST " + path + "\r\n"
    controlS.sendall(bytes(outMessage, "utf-8"))
    print(receive(controlS))
    print(receive(dataS))
    print(receive(controlS))

if(command == "rm"):
    dataS = openData(controlS)
    outMessage = "DELE " + path + "\r\n"
    controlS.sendall(bytes(outMessage, "utf-8"))
    print(receive(controlS))
    dataS.close()

if(command == "cp"):
    dataS = openData(controlS)
    if (firstParam):
        outMessage = "RETR " + path + "\r\n"
        controlS.sendall(bytes(outMessage, "utf-8"))
        f = open(param2, "w")
        while (1):
            inM = str(dataS.recv(1024), "utf-8")
            f.write(inM)
            if(not inM):
                break
        print(receive(controlS))
    else:
        outMessage = "STOR " + path + "\r\n"
        controlS.sendall(bytes(outMessage, "utf-8"))
        print(receive(controlS))
        f = open(param1)
        dataS.sendall(bytes(f.read(), "utf-8"))
        dataS.close()
        print(receive(controlS))

if (command == "mv"):
    dataS = openData(controlS)
    if (firstParam):
        outMessage = "RETR " + path + "\r\n"
        controlS.sendall(bytes(outMessage, "utf-8"))
        f = open(param2, "w")
        while (1):
            inM = str(dataS.recv(1024), "utf-8")
            f.write(inM)
            if(not inM):
                break
        print(receive(controlS))
        dataS = openData(controlS)
        outMessage = "DELE " + path + "\r\n"
        controlS.sendall(bytes(outMessage, "utf-8"))
        print(receive(controlS))
    else:
        outMessage = "STOR " + path + "\r\n"
        controlS.sendall(bytes(outMessage, "utf-8"))
        print(receive(controlS))
        f = open(param1)
        dataS.sendall(bytes(f.read(), "utf-8"))
        dataS.close()
        print(receive(controlS))
        os.remove(param1)

#quit
outMessage = "QUIT\r\n"
controlS.sendall(bytes(outMessage, "utf-8"))
print(receive(controlS))
controlS.close()