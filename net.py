from protobuf import fbr_pb2
from twisted.internet.error import ConnectionDone
from twisted.internet.protocol import Factory
from twisted.protocols.basic import Int32StringReceiver

class ProtobufProtocol(Int32StringReceiver):
    def sendMessage(self, message):
        #print("ProtobufProtocol: Sending")
        self.sendString(message.SerializeToString())
        #print("ProtobufProtocol: Sent")
  
    def stringReceived(self, data):
        #print("ProtobufProtocol: Received")
        message = fbr_pb2.network_message()
        message.ParseFromString(data)
        self.messageReceived(message)
    
    def messageReceived(self, message):
        print(message)
  
    def connectionMade(self):
        print("ProtobufProtocol: Connected")
    
    def connectionLost(self, reason=ConnectionDone):
        print("ProtobufProtocol: Connection Lost")
        print(reason)
    
class ProtobufProtocolFactory(Factory):
    def buildProtocol(self, addr):
        return ProtobufProtocol()