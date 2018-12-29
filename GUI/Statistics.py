'''
Statistics handler. Stores past times, able to display them, etc.
'''

# change this into real shared folder!
STORE_PATH = "../../../shared_folder"
# change if more scenarios are added
NO_SCENARIOS = 3

import wx
import jsonpickle
import sys
import matplotlib.pyplot as plt
import numpy as np

class Stat(object):
    def __init__ (self,scenario,time):
        self.scenario = scenario
        self.time = time

def sendStats(scenario,time):
    curStat = Stat(scenario,time)
    f = open(STORE_PATH+"/stats.json", 'ab+')
    f.seek(0,2)                                #Go to the end of file    
    if f.tell() == 0 :                         #Check if file is empty
        f.write(jsonpickle.encode([curStat]))      #If empty, write an array
    else :
        f.seek(-1,2)           
        f.truncate()                           #Remove the last character, open the array
        f.write(' , '.encode())                #Write the separator
        jsonpickle.set_encoder_options('json', indent = 0)
        f.write(jsonpickle.encode(curStat))      #Dump the entry
        f.write(']'.encode())    

def makeGraph():

    # decode collected stats from json file
    f = open(STORE_PATH+"/stats.json",'rb')
    json_str = f.read()
    try:
        dec_stats = jsonpickle.decode(json_str)
    except:
        sys.stderr.write('Could not decode the statistics file.\n')
        return

    # prepare all y values
    ymax = 0
    bins=[[] for i in range(NO_SCENARIOS)]
    for stat in dec_stats:
        # time is given in ms, converting to minutes
        conv = (stat.time/60000)%60
        bins[stat.scenario-1].append(conv)
        if conv > ymax:
            ymax = conv
    print ymax

    # prepare x axis, maybe this is not neeeded!
    xmax = 0
    for bin in bins:
        if len(bin) > xmax:
            xmax=len(bin)
    print xmax

    # actually make the graph
    # !!! THIS IS HARDCODED !!!
    fig, ax = plt.subplots ()
    ax.set_xlabel('Anzahl der bisher absolvierte Drills')
    ax.set_ylabel('benoetigte Zeit in Minuten')
    ax.set_title('Firedrill: Statistik')
    ax.plot(bins[0], 'bo', linestyle = 'dotted', label='Verbindungsprobleme')
    ax.plot(bins[1], 'go', linestyle = 'dotted', label='fehlendes Datenfile')
    ax.plot(bins[2], 'ro', linestyle = 'dotted', label='Tablespace')
    ax.set_xlim(0.8,xmax+0.2)
    ax.set_ylim(-0.2,ymax+2)
    xticks = [i+1 for i in range(xmax)]
    ax.set_xticks(xticks)
    ax.legend()

    fig.savefig(STORE_PATH+"/graph.png")

class StatisticsPanel(wx.Panel):

    def __init__(self, parent):
        
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition,size=parent.GetSize(), style = wx.TAB_TRAVERSAL )

        self.parent=parent

        # self.Update()

        backButton = wx.Button(self, wx.ID_ANY, "Zurueck", pos=(25,490))
        self.Bind(wx.EVT_BUTTON, self.OnBack, backButton)

    def OnBack(self,event):
        self.Hide()

    def Update(self):
        makeGraph()
        image = wx.Image(STORE_PATH+"/graph.png",wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self,wx.ID_ANY,wx.BitmapFromImage(image))


    