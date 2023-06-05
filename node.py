import json 
import time
import threading
import socket
import messagingFunctions as msgFunc
import sys

class Node:
    intialAddr = ("127.0.0.1",5000) #The address the first node will be assigned
    nodes = {} #Array to hold the current nodes in chat
    udpSocket = {} #Array to hold socket information that node has entered
    myName = "" #Name of node user assigns themselves

#Intial Node used to start the Peer to Peer Chat
    def startNode(self):
        msgFunc.convertToJSON(self.udpSocket,self.intialAddr,{
            "type":"newNode",
            "inputData":self.myName
        })

#Fucntion to allow node to recieve other node inputs in their chat
    def receiveChat(self):
        
        while 1:
            inputData, addr = msgFunc.receiveBytes(self.udpSocket)
            parse = json.loads(inputData)

            #Intial node in the chat will recieve this message when
            #a new node connects to the chat and the address of the
            #new node will be displayed
            if parse['type'] == 'newNode':
                print("**** A new node has connected to the chat ****")
                self.nodes[parse['inputData']]= addr
                print(addr)
                msgFunc.convertToJSON(self.udpSocket, addr,{
                    "type":'nodes',
                    "inputData":self.nodes
                })
            
            #The message each node will receive when a new node enters
            #the peer-to-peer chat
            if parse['type'] == 'nodes':
                print("**** The chat has received a new node ****")
                self.nodes.update(parse['inputData'])
                msgFunc.jsonBroadcast(self.udpSocket, {
                    "type":"welcome",
                    "inputData": self.myName
                },self.nodes)
            
            #When a new nodes has entered the chat, the intial node that
            #started the chat will receive a new message alongside their
            #IP address and Port Number
            if parse['type'] == 'welcome':
                self.nodes[parse['inputData']]= addr  
            
            #Shows other nodes still in the chat that that a specfic node has left
            #once they enter 'leave'
            if parse['type'] == 'leave':
                if(self.myName == parse['inputData']):
                    time.sleep(0.5) 
                    break
                #correctly shows the nodes present when a node has left
                self.nodes.pop(parse['inputData'])
                print(parse['inputData'] + " has left the chat. ****")         

            #All other input a node will receive while active on the chat
            if parse['type'] == 'input':
                print(parse['inputData'])  

     
#Function for Nodes in the chat to send messages to other nodes           
    def sendChat(self):
        while 1: 
            
            inputMessage = input("")
            splitMessage = inputMessage.split()
            
            #Allows every node on the chat to receive messages
            if splitMessage[-1] in self.nodes.keys():
                toAddr = self.nodes[splitMessage[-1]]
                joinMessage = ' '.join(splitMessage[:-1]) 
                msgFunc.jsonBroadcast(self.udp_socket, toAddr,{
                    "type":"input",
                    "inputData":joinMessage
                })   
            #Displays the name, address and port number of all 
            #nodes on the chat for that specfic user that typed nodes     
            if inputMessage == "nodes":
                print(self.nodes) 
                continue
            
            #Allow a node to type 'leave' and disconnect from the chat
            if inputMessage == "leave":
                msgFunc.jsonBroadcast(self.udpSocket, {
                    "type":"leave",
                    "inputData":self.myName
                },self.nodes)
                break
            
            #Allows the node to send a message to other on the chat
            else :
                msgFunc.jsonBroadcast(self.udpSocket, {
                    "type":"input",
                    "inputData":inputMessage
                },self.nodes)
                continue
             
def main():
    
    portNum = int(sys.argv[1])# Takes the port number first when ran in the terminal
    addrAndPort = ("127.0.0.1",portNum)
    userSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #The UDP/IP Socket used
    userSocket.bind((addrAndPort[0], addrAndPort[1])) #takes IP Address and Port defined in terminal
    
    node = Node()
    node.myName = sys.argv[2]# Takes the name the user assigns themselves as the second argument when ran in the terminal
    node.udpSocket = userSocket
    node.startNode()
    
    #Two threads start to handle both receiving and sending of messages in the chat
    threadOne = threading.Thread(target=node.receiveChat, args=())
    threadTwo = threading.Thread(target=node.sendChat, args=())
    threadOne.start()
    threadTwo.start()
    

if __name__ == '__main__':
    main()           