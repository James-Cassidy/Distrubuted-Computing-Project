import json

#This file is used to hold specfic messaging fucntions used in the main node file

#Converts string entered into bytes and sends to node addresses
def sendString(udpSocket, addr, msg):
  udpSocket.sendto(msg.encode('utf-8'),(addr[0], addr[1]))

#Recieve bytes (1024) and decode them
def receiveBytes(udpSocket):
  data, addr = udpSocket.recvfrom(1024)
  return data.decode('utf-8'), addr

#Convert message into a JSON String
def convertToJSON(udpSocket, addr, msg):
  sendString(udpSocket,addr,json.dumps(msg))

#Convert message to JSON Object to be broadcast
def jsonBroadcast(udpSocket, msg, nodes):
  for n in nodes.values():
    convertToJSON(udpSocket, n, msg)