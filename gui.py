import matplotlib
matplotlib.use('WXAgg')
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
from collections import deque
import numpy as np

class TelemetryWindow(wx.Frame):
    def __init__(self, parent):
        self.telemetry = None
        self.accel = deque(maxlen=100)
        self.rpm = deque(maxlen=100)
        self.line = None
        
        wx.Frame.__init__(self, parent, title="FBR-PC Telemetry Viewer", size=(640, 480))
        
        panel = wx.Panel(self, -1)
        
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Data Screen
        data_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Figures on LHS
        numbers_sizer = wx.FlexGridSizer(0, 2, 3, 3)
        numbers_sizer.AddGrowableCol(1)
        
        label = wx.StaticText(panel, label="Battery Voltage");
        self.voltage = wx.TextCtrl(panel, style=wx.TE_READONLY);
        numbers_sizer.Add(label, flag=wx.ALIGN_CENTER_VERTICAL)
        numbers_sizer.Add(self.voltage, flag=wx.EXPAND)
        
        label = wx.StaticText(panel, label="Coolant Temp");
        self.coolant_temp = wx.TextCtrl(panel, style=wx.TE_READONLY);
        numbers_sizer.Add(label, flag=wx.ALIGN_CENTER_VERTICAL)
        numbers_sizer.Add(self.coolant_temp, flag=wx.EXPAND)
        
        data_sizer.Add(numbers_sizer, proportion=0.5, flag=wx.EXPAND, border=3)
        
        # Graphs on RHS
        graph_sizer = wx.GridSizer(0, 1, 3, 3)
        
        self.revs_figure = Figure(None, None)
        self.revs_canvas = FigureCanvasWxAgg(panel, -1, self.revs_figure)
        
        self.g_figure = Figure(None, None)
        self.g_canvas = FigureCanvasWxAgg(panel, -1, self.g_figure)
        
        graph_sizer.Add(self.revs_canvas, flag=wx.EXPAND | wx.CENTER)#, flag=wx.EXPAND)
        graph_sizer.Add(self.g_canvas, flag=wx.EXPAND | wx.CENTER)
        
        data_sizer.Add(graph_sizer, proportion=1, flag=wx.EXPAND, border=3)
        
        top_sizer.Add(data_sizer, proportion=1, flag=wx.EXPAND)

        # Bottom Controls
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        btnStart = wx.Button(panel, label="Start")
        btnStop = wx.Button(panel, label="Stop")
        
        control_sizer.Add(btnStart, flag=wx.ALL, border=3)
        control_sizer.Add(btnStop, flag=wx.ALL, border=3)
        top_sizer.Add(control_sizer)
        
        self.revs_canvas.Bind(wx.EVT_IDLE, self.update_revs)
        self.g_canvas.Bind(wx.EVT_IDLE, self.update_g)
        
        btnStart.Bind(wx.EVT_BUTTON, self.btnStart_Click)
        btnStop.Bind(wx.EVT_BUTTON, self.btnStop_Click)
    
        panel.SetSizer(top_sizer)
    
    def update_revs(self, event=None):
        self.revs_figure.clear()
        plot = self.revs_figure.add_subplot(111)
        plot.plot(self.rpm)
        self.revs_canvas.draw()
    
    def update_g(self, event=None):        
        self.g_figure.clear()
        ax = self.g_figure.add_axes([0.1, 0.1, 0.8, 0.8,], polar=True)
        
        r = [np.linalg.norm(x) for x in self.accel]
        theta = [np.arctan2(x[1], x[0]) for x in self.accel]
        
        ax.plot(theta, r, color='#ee8d18', lw=3)
        #ax.plot(np.linspace(-np.pi, np.pi), np.ones(50))
        ax.set_rmax(2.0)
        self.g_canvas.draw()
    
    def process_message(self, message):
        self.telemetry = message;
        self.accel.append(np.array([self.telemetry.accel_x, self.telemetry.accel_y]))
        self.rpm.append(self.telemetry.rpm)
        self.voltage.SetValue("{:3.1f}".format(self.telemetry.voltage))
        self.coolant_temp.SetValue("{:3.1f}C".format(self.telemetry.coolant_temp))
        #print message
    
    def update_data(self, event=None):
        self.show_samples(self.live_buffer, self.live_buffer.maxlen)
    
    def show_samples(self, samples, width):
        if self.line is None or len(samples) < width:        
            plot = self.figure.add_subplot(111)
            plot.clear()
            plot.set_xlim(-width, 0)
            plot.set_ylim(0, 1024)
            plot.yaxis.tick_right()
            plot.set_yticks(range(0, 1025, 256))
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
