'''
Handles the scenario panel of the app -> start new Drill etc
'''

import wx
import Statistics
import Drill

class ScenarioPanel(wx.Panel):

    def __init__(self, parent):
        
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size=parent.GetSize(), style = wx.TAB_TRAVERSAL )

        self.parent = parent

        self.makeButtons()

        self.hints = self.loadHints(self.parent.scenario)
        self.noHints = 0

        description = self.loadDescription(self.parent.scenario)
        wx.StaticText(self,-1,description,(25,25))


    def makeButtons(self):
        self.startDrillButton = wx.Button(self,wx.ID_ANY,"Firedrill beginnen", pos = (25,100))
        self.endDrillButton = wx.Button(self, wx.ID_ANY, "Firedrill beenden", pos=(200,100))
        self.hintButton = wx.Button(self,wx.ID_ANY, "Hinweis",pos=(375,100))
        self.backButton = wx.Button(self,wx.ID_ANY, "Zurueck", pos=(25,400))

        self.Bind(wx.EVT_BUTTON, self.OnStartDrill, self.startDrillButton)
        self.Bind(wx.EVT_BUTTON, self.OnEndDrill, self.endDrillButton)
        self.Bind(wx.EVT_BUTTON, self.OnHint, self.hintButton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, self.backButton)
        self.hintButton.Disable()
        self.endDrillButton.Disable()

    def loadHints(self,scenario):
        # do someting with json files here, or hardcode
        print scenario
        example = ["Hint No. 1", "Hint No. 2", "Hint No.3"]
        return example

    def loadDescription(self,scenario):
        # do something with json files here, or hardcode
        example = "In diesem Szenario hat die Datenbank Hunger und moechte gefuettert werden.\nDafuer gibt es verschiedene Wege und verschiedene Ursachen."
        return example

    # Supposed to get the right UseCase, display according hints
    def OnHint(self,event):
        if self.noHints>=0:
            text = self.hints[self.noHints]
            wx.StaticText(self,-1,label = text, pos = (25,(150+self.noHints*25)))
            # no more hints
            if len(self.hints)==(self.noHints+1):
                self.noHints=-1
                self.hintButton.Disable()
            else:
                self.noHints+=1

        
    def OnStartDrill(self,event):
        dlg = wx.MessageDialog(self,"Im System ist etwas kaputt gegangen. Finde heraus, was es ist, und bringe es wieder zum laufen!")
        response = dlg.ShowModal()
        if response==wx.ID_OK:
            # starts Stop Watch
            self.watch = wx.StopWatch()
            print("Started StopWatch.")
            self.hintButton.Enable()
            self.endDrillButton.Enable()
            self.startDrillButton.Disable()
            self.backButton.Disable()

    def OnEndDrill(self,event):
        try:
            self.watch.Pause()
            dlg = wx.MessageDialog(self,"Ueberpruefen auf Integritaet des Systems...","Ueberpruefung...",wx.CANCEL)
            wait = dlg.ShowModal()
            if wait==wx.ID_CANCEL:
                self.watch.Resume()
            else:
                # replace with call to checkSystemFixed-bash script
                wx.CallLater(1500,self.endOfDrill)
        except AttributeError:
            wx.MessageBox(self,"Es laeuft kein Firedrill.", "Fehler", wx.OK | wx.ICON_ERROR)

    def endOfDrill(self):
        self.hintButton.Disable()
        self.endDrillButton.Disable()
        self.backButton.Enable()
        self.startDrillButton.Enable()
        self.curTime = self.watch.Time()
        dlg=wx.MessageDialog(self,"Das System ist wieder in Ordnung.","In Ordnung", wx.HELP)
        dlg.SetHelpLabel("&Benoetigte Zeit anzeigen")
        response = dlg.ShowModal()
        # put back in when working
        Statistics.sendStats(self.parent.scenario,self.curTime)
        self.parent.scenario = 0
        print self.curTime  
        if  response==wx.ID_HELP:
            wx.MessageBox("Das hat {} Stunden, {} Minuten und {} Sekunden gedauert.".format((self.curTime/3600000)%24,(self.curTime/60000)%60,(self.curTime/1000)%60))

    def OnBack(self,event):
        self.parent.scenario = 0
        self.Hide()



