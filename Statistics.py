############################################################################
#
# This file handles the statistics.
# Classes Stat and StatisticsPanel.
#
##############################################################################

import sys
import os
import wx
import jsonpickle
import matplotlib.pyplot as plt

# change this into actual shared folder!
STORE_PATH = "F:\repo\PG-hci"
# change if more scenarios are added
NO_SCENARIOS = 3

# Class for JSON
class Stat(object):
    def __init__(self, scenario, time, noHints, end_drills, succ):
        self.scenario = scenario
        self.time = time
        self.noHints = noHints # number of Hints used
        self.end_drills = end_drills #number of times endDrill was pressed
        self.succ = succ #success or not

# If we run into an error while trying to open the stats.json file, this function asks for the path to it. However, the path does not change permanently.
# Later, we should handle the path through a .config file, but for now, it is kept in a global variable above. To change it permanently, you have to change it in the code.
def specifyStorePath(parent, path):
    global STORE_PATH
    dlg = wx.MessageDialog(parent, "Der angegebene Pfad des shared folders ist "+STORE_PATH+".\n Ist dies richtig?", "Fehler...", wx.YES_NO | wx.ICON_ERROR)
    wait = dlg.ShowModal()
    if wait == wx.ID_YES:
        if not os.path.exists(STORE_PATH):
            os.makedirs(STORE_PATH)
        f = open(path, 'w+')
    else:
        dlg = wx.TextEntryDialog(parent, 'Bitte geben Sie den Pfad des shared folders an: ', 'Shared folder')
        dlg.SetValue("C:\\")
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            STORE_PATH = dlg.GetValue()
            if not os.path.exists(STORE_PATH):
                os.makedirs(STORE_PATH)
            path = os.path.join(STORE_PATH, 'stats.json')
            f = open(path, 'w+')
    f.close()

# This function writes the Statistics object into a JSON file
def sendStats(parent, scenario, time, hints_needed, times_ended, succ):
    curStat = Stat(scenario, time, hints_needed, times_ended, succ)
    path = os.path.join(STORE_PATH, 'stats.json')

    if not os.path.isfile(path):
        specifyStorePath(parent, path)

    f = open(path, 'ab+')
    # append Stat to json file (has to be done manually)
    f.seek(0, 2)                                #Go to the end of file
    if f.tell() == 0:                         #Check if file is empty
        f.write(jsonpickle.encode([curStat]))      #If empty, write an array
    else:
        f.seek(-1, 2)
        f.truncate()                           #Remove the last character, open the array
        f.write(' , '.encode())                #Write the separator
        jsonpickle.set_encoder_options('json', indent=0)
        f.write(jsonpickle.encode(curStat))      #Dump the entry
        f.write(']'.encode())
    f.close()

# This class handles the Statistics Panel i.e. it generates and shows the graph
class StatisticsPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=parent.GetSize(), style=wx.TAB_TRAVERSAL)

        self.parent = parent

        backButton = wx.Button(self, wx.ID_ANY, "Zurueck", pos=(25, 490))
        self.Bind(wx.EVT_BUTTON, self.OnBack, backButton)

    def OnBack(self, event):
        self.Hide()

    # this method needs to be called before showing the panel, otherwise it will be empty / the graph will be outdated
    def Update(self):
        ok = self.makeGraph()
        if ok:
            path = os.path.join(STORE_PATH, 'graph.png')
            image = wx.Image(path, wx.BITMAP_TYPE_PNG)
            wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image))
        else:
            wx.MessageBox("Der Statistik-Graph konnte nicht geladen werden. Wahrscheinlich liegt dies daran, dass noch keine Firedrills absolviert wurden.")

    def makeGraph(self):
        # decode collected stats from json file
        path = os.path.join(STORE_PATH, 'stats.json')

        if not os.path.isfile(path):
            specifyStorePath(self, path)
            wx.MessageBox("Es sind noch keine Daten vorhanden, die gezeigt werden koennten. Machen Sie erst ein paar Drills!")
            return False

        else:
            f = open(path, 'rb')
            json_str = f.read()
            try:
                dec_stats = jsonpickle.decode(json_str)
                f.close()
            except:
                sys.stderr.write('Could not decode the statistics file.\n')
                f.close()
                return False

            # prepare all y values
            ymax = 0
            bins = [[] for i in range(NO_SCENARIOS)]
            for stat in dec_stats:
                # why don't we make this distinction based on stat.succ?
                if stat.time:
                    # time is given in ms, converting to minutes
                    conv = (stat.time/60000)%60
                    bins[stat.scenario-1].append(conv)
                    if conv > ymax:
                        ymax = conv
                else:
                    # failed trial, will not appear in graph
                    pass
            print ymax

            # prepare x axis, maybe this is not neeeded!
            xmax = 0
            for bin in bins:
                if len(bin) > xmax:
                    xmax = len(bin)
            print xmax

            # actually make the graph
            fig, ax = plt.subplots()
            ax.set_xlabel('Anzahl der bisher absolvierte Drills')
            ax.set_ylabel('benoetigte Zeit in Minuten')
            ax.set_title('Firedrill: Statistik')

            # append a new scenario here
            ax.plot(bins[0], 'bo', linestyle='dotted', label='Verbindungsprobleme')
            ax.plot(bins[1], 'go', linestyle='dotted', label='fehlendes Datenfile')
            ax.plot(bins[2], 'ro', linestyle='dotted', label='Tablespace')

            ax.set_xlim(0.8, xmax+0.2)
            ax.set_ylim(-0.2, ymax+2)
            xticks = [i+1 for i in range(xmax)]
            ax.set_xticks(xticks)
            ax.legend()

            fig.savefig(STORE_PATH+"/graph.png")

            return True
