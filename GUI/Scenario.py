'''
Handles the scenario panel of the app -> start new Drill etc
'''

import wx
import Statistics
import Drill
import jsonpickle
import sys, os
import subprocess

class ScenarioJSON(object):
    def __init__ (self,description,hints):
        self.description = description
        self.hints = hints

class ScenarioPanel(wx.Panel):

    def __init__(self, parent, drillPanel):
        
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size=parent.GetSize(), style = wx.TAB_TRAVERSAL )

        self.parent = parent

        self.drillPanel = drillPanel

        self.makeButtons()

        self.scenario = self.parent.scenario

        self.hints, description = self.loadJSON()
        self.noHints = 0
        self.end_drills = 0
        wx.StaticText(self,-1,description,(25,25))


    def makeButtons(self):
        self.startDrillButton = wx.Button(self,wx.ID_ANY,"Firedrill beginnen", pos = (25,100))
        self.endDrillButton = wx.Button(self, wx.ID_ANY, "Firedrill beenden", pos=(200,100))
        self.hintButton = wx.Button(self,wx.ID_ANY, "Hinweis",pos=(375,100))
        self.backButton = wx.Button(self,wx.ID_ANY, "Zurueck", pos=(25,400))
        self.stopButton = wx.Button(self,wx.ID_ANY, "Drill abbrechen", pos = (25,135))

        self.Bind(wx.EVT_BUTTON, self.OnStartDrill, self.startDrillButton)
        self.Bind(wx.EVT_BUTTON, self.OnEndDrill, self.endDrillButton)
        self.Bind(wx.EVT_BUTTON, self.OnHint, self.hintButton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, self.backButton)
        self.Bind(wx.EVT_BUTTON, self.OnStop, self.stopButton)
        self.hintButton.Disable()
        self.endDrillButton.Disable()
        self.stopButton.Hide()

    def loadJSON(self):
        # decode scenario info from json file
        path = os.path.join('scenarios', str(self.scenario), 'info.json')
        print path
        try:
            f = open(path,'rb')
        except:
            wx.MessageBox("Something went wrong. Maybe the file is non-existent? Please contact the developers.")
            return
        json_str = f.read()
        try:
            dec_scenario = jsonpickle.decode(json_str)
        except:
            sys.stderr.write('Could not decode the info file.\n')
            return
        return dec_scenario.hints, dec_scenario.description

    # Supposed to get the right UseCase, display according hints
    def OnHint(self,event):
        if self.noHints>=0:
            text = self.hints[self.noHints]
            wx.StaticText(self,-1,label = text, pos = (25,(175+self.noHints*25)))
            # no more hints
            if len(self.hints)==(self.noHints+1):
                self.noHints=-1
                self.hintButton.Disable()
            else:
                self.noHints+=1

        
    def OnStartDrill(self,event):
        path = os.path.join('scenarios', str(self.scenario), 'startDrill.bat')
        print path
        out = subprocess.check_output(path,shell=True)
        print out
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
            self.stopButton.Show()

    def OnEndDrill(self,event):
        try:
            self.watch.Pause()
            dlg = wx.MessageDialog(self,"Ueberpruefen auf Integritaet des Systems...","Ueberpruefung...",wx.CANCEL)
            wait = dlg.ShowModal()
            if wait==wx.ID_CANCEL:
                self.watch.Resume()
            else:
                self.end_drills += 1
                path = os.path.join('scenarios', str(self.scenario), 'checkSystem.bat')
                print path
                out = subprocess.check_output(path,shell=True)
                print out
                # one might want to change this?
                if "True" in out:
                    self.endOfDrillSuccess()
                else:
                    dlg = wx.MessageDialog(self,"Das System ist noch nicht wieder in Ordnung. Probiere es mal anders.","Ueberpruefung...",wx.CANCEL)
                    wait = dlg.ShowModal()
                    if wait==wx.ID_CANCEL:
                        self.endOfDrillFailed()
                    else:
                        self.watch.Resume()
        except AttributeError:
            wx.MessageBox(self,"Es laeuft kein Firedrill.", "Fehler", wx.OK | wx.ICON_ERROR)

    def endOfDrillSuccess(self):
        self.hintButton.Disable()
        self.endDrillButton.Disable()
        self.backButton.Enable()
        self.startDrillButton.Enable()
        self.stopButton.Disable()
        self.curTime = self.watch.Time()
        dlg=wx.MessageDialog(self,"Das System ist wieder in Ordnung.","In Ordnung", wx.HELP)
        dlg.SetHelpLabel("&Benoetigte Zeit anzeigen")
        response = dlg.ShowModal()
        Statistics.sendStats(self,self.parent.scenario,self.curTime, self.noHints, self.end_drills, 1)
        self.parent.scenario = 0
        print self.curTime  
        if  response==wx.ID_HELP:
            wx.MessageBox("Das hat {} Stunden, {} Minuten und {} Sekunden gedauert.".format((self.curTime/3600000)%24,(self.curTime/60000)%60,(self.curTime/1000)%60))

    def endOfDrillFailed(self):
        self.hintButton.Disable()
        self.endDrillButton.Disable()
        self.backButton.Enable()
        self.startDrillButton.Enable()
        path = os.path.join('scenarios', str(self.scenario), 'fix.bat')
        print path
        out = subprocess.check_output(path,shell=True)
        print out
        Statistics.sendStats(self,self.parent.scenario,self.curTime, self.noHints, self.end_drills, 0)
        self.parent.scenario = 0
        wx.MessageBox("Der Originalzustand des Systems ist wiederhergestellt.")

    def OnStop(self,event):
        self.watch.Pause()
        self.endOfDrillFailed()

    def OnBack(self,event):
        self.parent.scenario = 0
        self.Hide()
        self.drillPanel.Show()




