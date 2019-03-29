#!/bin/python

###########################################################################################################
#
# This will create the Frame for the Tool. It sets the menu bar and sets up the Panels.
# Also, ths class keeps track of the current scenario so both DrillPanel and StatisticsPanel can access it.
#
###########################################################################################################

import wx
import Statistics
import Drill

class FiredrillFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(FiredrillFrame, self).__init__(*args, **kw)

        self.SetSize((680, 580))
        self.Centre()

        # keep track of the current scenario: 0 means none
        # this variable is modified and accessed by both DrillPanel and StatisticsPanel
        self.scenario = 0

        self.makeMenuBar()

        # Link both panels and hide the statistics panel. 
        # DrillPanel contains the buttons for the scenarios and is the starting point for doing a firedrill
        # StatisticsPanel accesses the shared folder specified in Statistics.py and plots a graph
        self.mainPanel = Drill.DrillPanel(self)
        self.statPanel=Statistics.StatisticsPanel(self)        
        self.statPanel.Hide()

    def makeMenuBar(self):

        statsMenu = wx.Menu()
        timesItem = statsMenu.Append(wx.ID_ANY, "&Statistik anzeigen...")

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        helpMenu.AppendSeparator()
        exitItem = helpMenu.Append(wx.ID_EXIT)

        menuBar = wx.MenuBar()
        menuBar.Append(statsMenu, "&Statistik")
        menuBar.Append(helpMenu, "&Hilfe")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnTimes, timesItem)

    def OnTimes(self,event):
        # Shows the statistics panel: plot new graph from data in shared folder specified in Statistics.py and show it
        self.statPanel.Update()
        self.statPanel.Show()


    def OnExit(self, event):
        # Close the frame, terminating the application.
        self.Close(True)

    def OnAbout(self, event):
        # Display an About Dialog
        wx.MessageBox("This is the prototype for a firedrill application supposed to be used in the work environment of system administrators.")


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = FiredrillFrame(None, title='Firedrill')
    frm.Show()
    app.MainLoop()