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
        telemetry = message.telemetry_message
        self.gui.process_message(telemetry)

class TelemetryProtocolFactory(Factory):
    def __init__(self, gui):
        self.protocol = TelemetryProtocol(gui)

app = wx.App(False)
frame = TelemetryWindow(None)
frame.Show(True)
reactor.registerWxApp(app)

endpoint = clientFromString(reactor, sys.argv[1])
endpoint.connect(TelemetryProtocolFactory(frame))

for i in np.linspace(-np.pi, np.pi):
    message = network_message()
    
    message.telemetry.accel_x = np.cos(i)
    message.telemetry.accel_y = np.sin(i)
    
    frame.process_message(message)

reactor.run()