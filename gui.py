import matplotlib
matplotlib.use('WXAgg')
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
from collections import deque

class ControlWindow(wx.Frame):
    def __init__(self, parent):
        self.line = None
        self.live_buffer = deque(maxlen=5000)
        
        wx.Frame.__init__(self, parent, title="FBR-PC Telemetry Viewer", size=(640, 480))
        
        panel = wx.Panel(self, -1)
        
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        data_sizer = wx.FlexGridSizer(1, 2, 3, 3)
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        btnStart = wx.Button(panel, label="Start")
        btnStop = wx.Button(panel, label="Stop")
        
        control_sizer.Add(btnStart, flag=wx.ALL, border=3)
        control_sizer.Add(btnStop, flag=wx.ALL, border=3)
        
        lblRPM = wx.StaticText(panel, label="RPM")
        
        guaRPM = wx.Gauge(panel)
        guaRPM.SetRange(13000)
        guaRPM.SetValue(2000)
        
        data_sizer.AddGrowableCol(1)
        
        for i in range(0, 10):
            label = wx.StaticText(panel, label="Control #{}".format(i))
            gauge = wx.Gauge(panel, range=10)
            gauge.SetValue(i)        
            data_sizer.Add(label, flag=wx.ALIGN_CENTER_VERTICAL)
            data_sizer.Add(gauge, flag=wx.EXPAND)
        
        data_sizer.Add(lblRPM, flag=wx.ALIGN_CENTER_VERTICAL)
        data_sizer.Add(guaRPM)
        
        top_sizer.Add(data_sizer, flag=wx.ALL | wx.EXPAND, border=3)
        top_sizer.Add(control_sizer)
        
        #self.canvas.Bind(wx.EVT_IDLE, self.update_data)
        btnStart.Bind(wx.EVT_BUTTON, self.btnStart_Click)
        btnStop.Bind(wx.EVT_BUTTON, self.btnStop_Click)
    
        panel.SetSizer(top_sizer)
    
    def update_data(self, event=None):
        self.show_samples(self.live_buffer, self.live_buffer.maxlen)
    
    def show_samples(self, samples, width):
        if self.line is None or len(samples) < width:        
            plot = self.figure.add_subplot(111)
            plot.clear()
            plot.set_xlim(-width, 0)
            plot.set_ylim(0, 1024)
            plot.yaxis.tick_right()
            plot.set_yticks(range(0,1025,256))
            line, = plot.plot(range(-len(samples), 0), samples)
            
            if len(samples) == width:
                self.line = line
            else:
                self.line = None    
        else:
            self.line.set_ydata(samples)

        self.canvas.draw()
    
    def btnStart_Click(self, event=None):
        pass
    
    def btnStop_Click(self, event=None):
        pass
