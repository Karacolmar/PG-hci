'''
Handles the main panel of the app -> start new Drill etc
'''

import wx

class DrillPanel(wx.Panel):

    def __init__(self, parent):
        
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size=parent.GetSize(), style = wx.TAB_TRAVERSAL )

        self.Database = False
        self.Update = False

        self.makeButtons()

    def makeButtons(self):
        startDrillButton = wx.Button(self, wx.ID_ANY, "Start new firedrill", pos=(25,150))
        endDrillButton = wx.Button(self, wx.ID_ANY, "End firedrill", pos=(25,200))
        self.hintButton = wx.Button(self,wx.ID_ANY, "Hint",pos=(25,250))

        self.Bind(wx.EVT_BUTTON, self.OnStartDrill, startDrillButton)
        self.Bind(wx.EVT_BUTTON, self.OnEndDrill, endDrillButton)
        self.Bind(wx.EVT_BUTTON, self.OnHint, self.hintButton)
        self.hintButton.Disable()

    # Supposed to get the right UseCase, display according hints
    def OnHint(self,event):
        if self.Update or self.Database:
            wx.MessageBox("Start by looking into the logs...")
        
    def OnStartDrill(self,event):
        dlg = wx.MessageDialog(self, "Which scenario do you want to train?", "Start a new Drill", wx.YES_NO|wx.CANCEL)
        dlg.SetYesNoLabels("&Update", "&Database")
        response = dlg.ShowModal()
        # Update case
        if response == wx.ID_YES:
            self.Database = False
            self.Update = True
            self.startDrill()
        # Database case
        elif response == wx.ID_NO:
            self.Update = False
            self.Database = True
            self.startDrill()

    def startDrill(self):
        dlg = wx.MessageDialog(self,"Something in your system broke. Find out what it is!")
        response = dlg.ShowModal()
        if response==wx.ID_OK:
            # starts Stop Watch
            self.watch = wx.StopWatch()
            print("Started StopWatch.")
            self.hintButton.Enable()

    def OnEndDrill(self,event):
        try:
            self.watch.Pause()
            dlg = wx.MessageDialog(self,"Checking whether your fix was successful...","Checking...",wx.CANCEL)
            wait = dlg.ShowModal()
            if wait==wx.ID_CANCEL:
                self.watch.Resume()
            else:
                # replace with call to checkSystemFixed-bash script
                wx.CallLater(1500,self.endOfDrill)
        except AttributeError:
            wx.MessageBox(self,"You have not started a firedrill yet.", "Error", wx.OK | wx.ICON_ERROR)

    def endOfDrill(self):
        dlg=wx.MessageDialog(self,"Your system is back to normal.","Well done", wx.HELP)
        dlg.SetHelpLabel("&Display Time")
        response = dlg.ShowModal()
        self.curTime = self.watch.Time()
        print self.curTime  
        if  response==wx.ID_HELP:
            wx.MessageBox("It took you {} hours, {} minutes and {} seconds.".format((self.curTime/3600000)%24,(self.curTime/60000)%60,(self.curTime/1000)%60))


