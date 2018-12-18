'''
Handles the main panel of the app -> start new Drill etc
'''

import wx
import Statistics
import Scenario

class DrillPanel(wx.Panel):

    def __init__(self, parent):
        
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size=parent.GetSize(), style = wx.TAB_TRAVERSAL )

        self.parent = parent

        self.makeButtons()

    def makeButtons(self):
        self.startDrill1Button = wx.Button(self, wx.ID_ANY, "Verbindungsprobleme", pos=(50,250))
        self.startDrill2Button = wx.Button(self,wx.ID_ANY, "fehlendes Datenfile", pos=(200,250))
        self.startDrill3Button = wx.Button(self,wx.ID_ANY, "Tablespace", pos=(350,250))
        self.exploreButton = wx.Button(self,wx.ID_ANY,"Lerne Oracle kennen", pos=(50,150))

        # maybe it is not possible to get which button was pressed - then we need three managing functions for this stuff
        self.Bind(wx.EVT_BUTTON, self.OnStartDrill, self.startDrill1Button)
        self.Bind(wx.EVT_BUTTON, self.OnStartDrill, self.startDrill2Button)
        self.Bind(wx.EVT_BUTTON, self.OnStartDrill, self.startDrill3Button)
        self.Bind(wx.EVT_BUTTON, self.OnExplore, self.exploreButton)

    # Einfuehrungsding von Leo
    def OnExplore(self,event):
        wx.MessageBox("This will be possible soon.")
        
    def OnStartDrill(self,event):
        which = event.GetEventObject().GetLabel()
        if "1" in which:
            self.parent.scenario = 1
        elif "2" in which:
            self.parent.scenario = 2
        elif "3" in which:
            self.parent.scenario = 3        
        self.startDrill()

    def startDrill(self):
        self.scenarioPanel=Scenario.ScenarioPanel(self.parent)
        self.scenarioPanel.Show()


