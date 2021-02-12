import socket
import sys

def parseUrl(url):
    # parses urls of the format ftp://[USER[:PASSWORD]@]HOST[:PORT]/PATH
    param = url[:6]
    #first check for username/password
    temptuple = param.partition('@')
    plc = 0
    if (temptuple[1] == '@'):
        param = temptuple[2]
        temptuple = temptuple[0].partition(':')
        #adding a beginning code so I can tell which things are included later
        paramlist[plc] = "us:" + ((string)(temptuple[0]))
        plc += 1
        paramlist[plc] = "ps:" + ((string)(temptuple[2]))
        plc += 1
    else:
        #then check for port
        param = temptuple[0]
        temptuple = param.partition(':')
        if (temptuple[1] == ':'):
            paramlist[plc] = "ho:" + ((string)(temptuple[0]))
            plc += 1
            temptuple = temptuple[2].partition('/')
            paramlist[plc] = "po:" + ((string)(temptuple[0]))
            plc += 1
            paramlist[plc] = "pt:/" + ((string)(temptuple[2]))
        else:
            temptuple = temptuple[0].partition('/')
            paramlist[plc] = "ho:" + ((string)(temptuple[0]))
            plc += 1
            paramlist[plc] = "pt:/" + ((string)(temptuple[2]))
    return paramlist

#receives a message from socket s, and returns with said message
def receive(s)
    inMessage = ""
    while(receiving):
        inMessage += str(s.recv(1024), "utf-8")
        if(inMessage.endswith('\r\n')):
            receiving = False
    return inMessage

#Parse the command and inputs
syslen = len(sys.argv)
assert (sys.argv[0] == "./3700ftp"), "Invalid command"
if (syslen == 3):
    command = sys.argv[1]
    param1 = sys.argv[2]
else if (syslen == 4):
    command = sys.argv[1]
    param1 = sys.argv[2]
    param2 = sys.argv[3]
else:
    return -1

if (param1[:6] == 'ftp://')
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



s = socket.socket()
s.connect((host, port))

print(receive(s))

outMessage = "USER " + username + "\r\n"
s.sendall(bytes(outMessage, "utf-8"))
inMessage = receive(s)
print(inMessage)
if(inMessage[:3] != "230"):
    outMessage = "PASS " + password + "\r\n"
    s.sendall(bytes(outMessage, "utf-8"))
outMessage = "TYPE I\r\n"
s.sendall(bytes(outMessage, "utf-8"))
print(receive(s))
outMessage = "MODE S\r\n"
s.sendall(bytes(outMessage, "utf-8"))
print(receive(s))
outMessage = "STRU F\r\n"
s.sendall(bytes(outMessage, "utf-8"))
print(receive(s))

#run the commands
if(command == "ls"):
    outMessage = "LIST " + path + "\r\n"
    s.sendall(bytes(outMessage, "utf-8"))
    print(receive(s))
    print("completed ls")
else:
    print("got past ls")
    return -1

#quit
outMessage = "QUIT\r\n"
s.sendall(bytes(outMessage, "utf-8"))
print(receive(s))

print("finished and quit")