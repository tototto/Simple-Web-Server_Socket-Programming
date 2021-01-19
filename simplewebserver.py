# Write down your name:
# Write down your student number: A

from socket import *
import sys

def MatchFile(clientFileName):
    return clientFileName == "/index.html";

def isValid_Http_req(clientHTTP):
    return clientHTTP == "HTTP/1.0" or clientHTTP == "HTTP/1.1";

def isValid_Header(client_Header):
    return client_Header == "HEAD";

def Result_of_Client_Req(FileName_Requested, Http_Version_used, Client_Req_Header):
    return (MatchFile(FileName_Requested) and isValid_Http_req(Http_Version_used) and isValid_Header(Client_Req_Header)), MatchFile(FileName_Requested);

# port can be specified on command line. If omitted, it defaults to 12345
# you can also modify the code here to change the port if you do not want to
# use command line arguments

if len(sys.argv) > 1:
    serverPort = int(sys.argv[1])
else:
    serverPort = 12345

# create socket
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', serverPort))

serverSocket.listen(1)

print('Server is ready to receive message')

connectionSocket, clientAddr = serverSocket.accept()

while True:

    # receive message of size 2048 in terms of bytes
    message = connectionSocket.recv(2048)

    # To decode the message
    message = message.decode()

    print(message)

    # read and parse request
    FirstLine = (message.split('\r\n'))[0]
    Client_Req_Header = (FirstLine.split(' '))[0]
    FileName_Requested = (FirstLine.split(' '))[1]
    Http_Version_used = (FirstLine.split(' '))[2]

    # response String to send
    response200 = '200 OK\r\nDate: Wed, 23 Jan 2019 13:11:15 GMT\r\n\
    Content-Length: 606\r\nContent-Type: text/html\r\n\r\n'

    response404 = '404 Not Found\r\nContent-Length: 0\r\n\r\n'

    # Ascertain client request and provide response
    Overall_Result, fileName_Match = Result_of_Client_Req(FileName_Requested, Http_Version_used, Client_Req_Header)

    if Overall_Result:
        connectionSocket.send(response200.encode())
        print(response200)
    elif fileName_Match == False:
        connectionSocket.send(response404.encode())

    # if HTTP 1.0 close TCP
    if Http_Version_used == "HTTP/1.0":
        connectionSocket.close()
        break

# if 1.1 keep the TCP connection open forever.