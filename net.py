from protobuf import fbr_pb2
from twisted.protocols.basic import IntNStringReceiver
from twisted.internet.error import ConnectionDone
from twisted.internet.protocol import Factory
from struct import calcsize

class ProtobufProtocol(IntNStringReceiver):
    structFormat = "<I"
    prefixLength = calcsize(structFormat)
    
    def sendMessage(self, message):
        #print("ProtobufProtocol: Sending")
        self.sendString(message.SerializeToString())
        #print("ProtobufProtocol: Sent")
  
    def stringReceived(self, data):
        #print("ProtobufProtocol: Received {} bytes".format(len(data)))
        message = fbr_pb2.telemetry_message()
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