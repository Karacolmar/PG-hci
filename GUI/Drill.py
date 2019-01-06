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

    # Einfuehrung in Oracle
    def OnExplore(self,event):
	def IntroDialog(Intro):
		frame = wx.Frame(None, -1, 'win.py')
		frame.SetDimensions(0,0,200,50)
		x = ""
		# Installationspfad
		if Intro == 1:
			dlg = wx.TextEntryDialog(frame, 'Finden Sie heraus wo Oracle installiert wurde($ORACLE_BASE).','Einleitung 1/4')
			dlg.SetValue("C:\\")
			result = dlg.ShowModal()
			if result == wx.ID_OK:
			    print('## Einleitung: 1/4 : %s' % dlg.GetValue())
			    x = dlg.GetValue()
			else:
			    return result

		#Homeverzeichnis
		if Intro == 2:
			dlg = wx.TextEntryDialog(frame, 'Wo liegt das Oracle-Homeverzeichnis $ORACLE_HOME?','Einleitung 2/4')
			dlg.SetValue("C:\\app\\ora12")
			result = dlg.ShowModal()
			if result == wx.ID_OK:
			    print "ok"
			    x = dlg.GetValue()
			    print('## Einleitung: 2/4 : %s' % x)
			else:
			    return result

		#Datentypen
		if Intro == 3:
			dlg = wx.TextEntryDialog(frame, 'Wo liegen die menschenlesbaren Parameterfiles?','Einleitung 3/4')
			dlg.SetValue("D:\\oracle")
			result = dlg.ShowModal()
			if result == wx.ID_OK:
			    x = dlg.GetValue()
			    print('## Einleitung: 3/4 : %s' % x)
			else:
			    return result

		#Speicher
		if Intro == 4:
			dlg = wx.TextEntryDialog(frame, 'Wie viele MB Speicher hat unser Tablespace (abgerundet)?','Einleitung 4/4')
			dlg.SetValue("1024")
			result = dlg.ShowModal()
			if result == wx.ID_OK:
			    x = dlg.GetValue()
			    print('## Einleitung: 4/4 : %s' % x)
			else:
			    return result
		if Intro == 5:
		#mehr erwuenscht?
			return "MEHR"
		dlg.Destroy()
		return x

        dlg = wx.MessageDialog(self, "Es folgt eine kurze allgemeine Einleitung in Oracle",'Einleitung',wx.CANCEL | wx.ICON_INFORMATION)
	result = dlg.ShowModal()
	 
	if result == wx.ID_OK:
		wx.MessageBox("Die Oraclesoftware trennt zwischen Datenbanksystem und Instanzen. \nMehrere Versionen von Oracle koennen so installiert und fuer verschiedene Instanzen benutzt werden.\nDie Instanz innerhalb unseres Firedrills ist KHV.",'Einleitung 1/4', wx.OK)
		while 1:
			Pfad = IntroDialog(1)	    	
			if  Pfad == "C:\\app\\ora12":
				print "## Einleitung: Installationspfad OK\n"
				
				break	
			if Pfad == wx.ID_CANCEL:
				print "## Einleitung: 1/4 Abbruch\n"
				return
		wx.MessageBox("Unterordner:\n\\product - Beinhaltet installierte Datenbankensysteme.\n\\admin - Hier liegen die Parameterfiles(pfile) und man kann Justierungen an den Instanzen vornehmen. \n\\diag - Speicherort der Log- und Tracefiles.",'Einleitung 2/4', wx.OK)
		
		while 2:
			Pfad = IntroDialog(2)
			if  Pfad == "C:\\app\\ora12\\product\\12.0.1\\db_1":
				print "## Einleitung: OracleHome OK\n"
				
				break
			if Pfad == wx.ID_CANCEL:
				print "## Einleitung: 2/4 Abbruch\n"
				return	
		wx.MessageBox("5 wichtige Dateitypen\nDatafiles: Daten\nControlfiles: 2-3 je Installation, in verschiedenen Orten (menschenlesbar: pfiles)\nRedologfiles: Transaktionsfiles als Rollbackanleitung\nAchivelogfiles: archivierte Redologfiles, Lebensdauer ist bis Vollsicherung\nTracefiles: andere Logdateien",'Einleitung 3/4', wx.OK)

		while 3:
			Pfad = IntroDialog(3)
			if  Pfad == "D:\\oracle\\admin\\khv\\pfile":
				print "## Einleitung: pfilespfad OK\n"
				
				break
		if Pfad == wx.ID_CANCEL:
				print "## Einleitung: 3/4 Abbruch\n"
				return
		wx.MessageBox("Oracle hat eine eigene Speicherstruktur.\nDie kleinste Einheit ist ein OSBlock.\nDanach gibt es die Oraclebloecke, Extents, Segments und die Tablespaces.\nTablespaces definieren die Datenmenge der Instanz und werden normalerweise nach einem Muster (Bspw.: \"dfSID01.dbf\") benannnt",'Einleitung 4/4', wx.OK)
		while 4:
			Pfad = IntroDialog(4)
			if  Pfad == "1024":
				print "## Einleitung: Speicher OK\n"
				
				break
		if Pfad == wx.ID_CANCEL:
				print "## Einleitung: 4/4 Abbruch\n"
				return	
	else:
		print "## Einleitung: 0/4 Abbruch"
	        return
		
	print "## Einleitung: erfolgreich beendet"
        return

    def OnViewDrill(self,event):
        self.parent.scenario = event.GetId()
        self.scenarioPanel=Scenario.ScenarioPanel(self.parent)
        self.scenarioPanel.Show()


