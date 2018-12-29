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
        self.Drill1Button = wx.Button(self, 1, "Verbindungsprobleme", pos=(50,250))
        self.Drill2Button = wx.Button(self,2, "fehlendes Datenfile", pos=(200,250))
        self.Drill3Button = wx.Button(self,3, "Tablespace", pos=(350,250))
        self.exploreButton = wx.Button(self,wx.ID_ANY,"Lerne Oracle kennen", pos=(50,150))

        # maybe it is not possible to get which button was pressed - then we need three managing functions for this stuff
        self.Bind(wx.EVT_BUTTON, self.OnViewDrill, self.Drill1Button)
        self.Bind(wx.EVT_BUTTON, self.OnViewDrill, self.Drill2Button)
        self.Bind(wx.EVT_BUTTON, self.OnViewDrill, self.Drill3Button)
        self.Bind(wx.EVT_BUTTON, self.OnExplore, self.exploreButton)

    # Einfuehrungsding von Leo
    def OnExplore(self,event):
        wx.MessageBox("This will be possible soon.")
        
    def OnViewDrill(self,event):
        self.parent.scenario = event.GetId()
        self.scenarioPanel=Scenario.ScenarioPanel(self.parent)
        self.scenarioPanel.Show()


