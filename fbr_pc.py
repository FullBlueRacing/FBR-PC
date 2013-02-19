from twisted.internet import wxreactor
wxreactor.install()

import sys
from net import ProtobufProtocol
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import clientFromString
from gui import ControlWindow
import wx

class TelemetryProtocol(ProtobufProtocol):
    pass

class TelemetryProtocolFactory(Factory):
    def __init__(self):
        self.protocol = TelemetryProtocol()

endpoint = clientFromString(reactor, sys.argv[1])
endpoint.connect(TelemetryProtocolFactory())

app = wx.App(False)
frame = ControlWindow(None)
frame.Show(True)
reactor.registerWxApp(app)

reactor.run()