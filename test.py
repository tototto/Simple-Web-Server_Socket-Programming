from socket import *
import sys
import time

# test case ID can be specified on command line as the first argument. If omitted, it defaults to 1 (the first test case)
if len(sys.argv) > 1:
  reqId = int(sys.argv[1])
else:
  reqId = 4

# port can be specified on command line as the second argument. If omitted, it defaults to 12345
# you can also modify the code here to change the port if you do not want to
# use command line arguments
if len(sys.argv) > 2:
  serverPort = int(sys.argv[2])
else:
  serverPort = 12345

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('', serverPort))

reqs = [
  "HEAD /index.html HTTP/1.0\r\nHost: www.example.org\r\nConnection: keep-alive\r\n\r\n", 
  "HEAD /favicon.png HTTP/1.0\r\nHost: www.example.org\r\nConnection: keep-alive\r\n\r\n", 
  "HEAD /index.html HTTP/1.0\r\nHost: www.example.org\r\nConnection: keep-alive\r\n\r\nHEAD /favicon.png HTTP/1.0\r\nHost: www.example.org\r\nConnection: keep-alive\r\n\r\n",
  #
  "HEAD /index.html HTTP/1.1\r\nHost: www.example.org\r\nConnection: keep-alive\r\n\r\n", 
  "HEAD /favicon.png HTTP/1.1\r\nHost: www.example.org\r\nConnection: keep-alive\r\n\r\n"
]

def testHttp(clientSocket, req, prepass, prefail):
  rtn = 0
  print(req.strip())
  print()

  clientSocket.send(req.encode())
  buf = clientSocket.recv(1024)
  if len(buf) == 0:
    print("connection is closed by the client")
    return 0
  if len(buf) <= 4:
    print("invalid response: too short");
    return 0
  if buf[-4:] != b'\r\n\r\n':
    print("response is not properly ended.")
    return 0
  lns = buf.decode().split('\r\n')
  ln1 = lns[0]

  if req.startswith('HEAD /index.html '):
    if ln1.startswith('200 '):
      rtn = 1
      print('%s expect status 200, got 200' % prepass)
    else:
      rtn = 0
      print('%s expect status 200, got "%s"' % (prefail, ln1))
  else:
    if ln1.startswith('404 '):
      rtn = 1
      print('%s expect status 404, got 404' % prepass)
    else:
      rtn = 0
      print('%s expect status 404, got "%s"' % (prefail, ln1))
  if req.find('HTTP/1.0\r\n') >= 0:
    clientSocket.settimeout(1)
    connClosed = False
    try:
      buf = clientSocket.recv(1)
      connClosed = (len(buf) == 0)
    except:
      # timed out
      connClosed = False
    if connClosed:
      print("Server closed connection after processing an HTTP/1.0 request.")
    else:
      rtn = 0
      print("Error: server not closing connection after processing an HTTP/1.0 request.")
  print()
  return rtn

if reqId <= 3:
  print('Test #%d (HTTP/1.0): ' % reqId)
  testHttp(clientSocket, reqs[reqId-1], "Test passed: ", "Test failed: ")
else:
  print("Test #4 (HTTP/1.1): ")
  reqId = 4
  s1 = testHttp(clientSocket, reqs[reqId-1], "-- ", "-- ")
  reqId = 5
  s2 = testHttp(clientSocket, reqs[reqId-1], "-- ", "-- ")
  if s1 and s2:
    print("HTTP/1.1 test passed")
  else:
    print("HTTP/1.1 test failed")

