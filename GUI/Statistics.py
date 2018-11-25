'''
Statistics handler. Stores past times, able to display them, etc.
'''

import wx

class StatisticsPanel(wx.Panel):

    def __init__(self, parent):
        
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition,size=parent.GetSize(), style = wx.TAB_TRAVERSAL )

        self.parent=parent

        image = wx.Image('stat_demo.png',wx.BITMAP_TYPE_PNG)
        imageBitmap = wx.StaticBitmap(self,wx.ID_ANY,wx.BitmapFromImage(image))

        backButton = wx.Button(self, wx.ID_ANY, "Back", pos=(25,375))
        self.Bind(wx.EVT_BUTTON, self.OnBack, backButton)

    def OnBack(self,event):
        self.Hide()
        self.parent.mainPanel.Show()



    