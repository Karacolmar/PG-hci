'''
Statistics handler. Stores past times, able to display them, etc.
'''

import wx
import jsonpickle
import sys
import matplotlib.pyplot as plt

class Stat(object):
    def __init__ (self,scenario,time):
        self.scenario = scenario
        self.time = time

# PATH NOT SPECIFIED, DOES NOT WORK LIKE THIS
def sendStats(scenario,time):
    curStat = Stat(scenario,time)
    resf = open("/path/to/shared/folder/statistics.json", 'w')
    jsonpickle.set_encoder_options('json', indent = 0)
    resf.write(jsonpickle.encode(curStat))

def makeGraph():
    f = open("/path/to/shared/folder/statistics.json",'rb')
    json_str = f.read()
    try:
        dec_stats = jsonpickle.decode(json_str)
    except:
        sys.stderr.write('Could not decode the statistics file.\n')
        return
    # DO STUFF HERE


class StatisticsPanel(wx.Panel):

    def __init__(self, parent):
        
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition,size=parent.GetSize(), style = wx.TAB_TRAVERSAL )

        self.parent=parent

        # replace by loading stuff
        image = wx.Image('stat_demo.png',wx.BITMAP_TYPE_PNG)
        imageBitmap = wx.StaticBitmap(self,wx.ID_ANY,wx.BitmapFromImage(image))

        backButton = wx.Button(self, wx.ID_ANY, "Zurueck", pos=(25,400))
        self.Bind(wx.EVT_BUTTON, self.OnBack, backButton)

    def OnBack(self,event):
        self.Hide()



    