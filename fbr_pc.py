from twisted.internet import wxreactor
wxreactor.install()

import sys
from net import ProtobufProtocol
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import clientFromString
from gui import TelemetryWindow
from protobuf.fbr_pb2 import network_message
import wx
import numpy as np

class TelemetryProtocol(ProtobufProtocol):
    def __init__(self, gui):
        self.gui = gui
        
    def messageReceived(self, message):
        #print("Message Received")
        telemetry = message
        self.gui.process_message(telemetry)

class TelemetryProtocolFactory(Factory):
    def __init__(self, gui):
        self.protocol = TelemetryProtocol(gui)
    
    def buildProtocol(self, addr):
        print(addr)
        return self.protocol

app = wx.App(False)
frame = TelemetryWindow(None)
frame.Show(True)
reactor.registerWxApp(app)

#endpoint = clientFromString(reactor, sys.argv[1])           UNCOMMENT!!!
#endpoint.connect(TelemetryProtocolFactory(frame))			 UNCOMMENT!!!		

#endpoint = TCP4ServerEndpoint(reactor, 8282)
#endpoint.listen(TelemetryProtocolFactory(frame))

#for i in np.linspace(-np.pi, np.pi):
#    message = network_message()
#    
#    message.telemetry.accel_x = np.cos(i)
#    message.telemetry.accel_y = np.sin(i)
#    
#    frame.process_message(message)

reactor.run()