import win32file
import time, os
import urllib, urllib2
import base64
import pickle
import subprocess
import wx

class LocClient(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="H1Z1 Map Client", pos=(150,150), size=(350,200))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.panel = wx.Panel(self)
        self.updateText = wx.TextCtrl(self.panel,style=wx.TE_MULTILINE)
        ## Add button to start scan
        ## add parameters (server address, character name, screenshot folder button, sending status) and save button


        self.ServerAddr = "http://ghoknhar.com"
        ## H1Z1 ScreenShot Folder
        self.updateText.AppendText("Loading ScreenShot Folder...\n")

        try:
            self.screenshotFolder = pickle.load(open("save.p","rb"))
            if not os.path.exists(self.screenshotFolder):
                self.updateText.AppendText("Save file path not valid. Running Search...")
                self.GetPath()
        except:
            self.updateText.AppendText("Finding screen shot file path\n")
            self.GetPath()
        self.updateText.AppendText("Screen shot folder loaded\n")
        ## Files Currently in folder
        self.currentFiles = dict([(f, None) for f in os.listdir(self.screenshotFolder)])
        ## file to send to server
        self.newFile = None

    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def GetPath(self):
        ## Find all storage drives for search
        userDrives = []
        driveList = subprocess.Popen('wmic logicaldisk get name,description', shell=True, stdout=subprocess.PIPE)
        driveListo, err = driveList.communicate()
        driveLines = driveListo.split('\n')
        # Extract Local Storage Devices
        for item in driveLines:
            if item.startswith('Local'):
                userDrives.append(item[item.index(':')-1]+':')
        # Search Storage Devices for H1Z1 ScreenShot Folder
        for HD in userDrives:
            for dirName, dirNames, fileNames in os.walk(HD):
                for subDirName in dirNames:
                    # Find H1Z1 Steam folder
                    if subDirName == "295110":
                        self.screenshotFolder = os.path.join(dirName,subDirName)+"\screenshots"
                        self.updateText.AppendText("Screen Shot Folder Found")
                        # Save path
                        pickle.dump(self.screenshotFolder,open("save.p","wb"))
                        self.updateText.AppendText("Saved for future use")
                        return
        self.updateText.AppendText("Could not find screen shots folder!")

    def SetConnection(self):
        pass

    def SendFile(self):
        ## Not done.
        try:
            self.newFile
            with open(self.newFile, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read())
            raw_params = {'quality':'2','category':'1','debug':'0', 'image': encoded_image}
            params = urllib.urlencode(raw_params)
            request = urllib2.Request(self.serverAddr, params)
            request.add_header("Content-type", "application/x-www-form-urlencoded; charset=UTF-8")

        except Exception as e:
            self.updateText.AppendText("Error sending file! " + e)

    def Scan(self):
        #Will Crash wxpy after 5 or so Scans.. whyyyyy
        self.updateText.AppendText("Scanning...")
        while 1:
            time.sleep (1)
            after = dict ([(f, None) for f in os.listdir(self.screenshotFolder)])
            added = [f for f in after if not f in self.currentFiles]
            removed = [f for f in self.currentFiles if not f in after]
            if added: self.updateText.AppendText("Added: ", ", ".join(added))
            if removed: self.updateText.AppendText("Removed: ", ", ".join(removed))
            before = after
            self.updateText.AppendText("hue\n")
            print "hue"

class AboutBox(wx.Dialog):
    #Not in use yet
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About H1Z1 Map Client",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400,200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

if __name__ == '__main__':
    app = wx.App(redirect=True)
    Client = LocClient()
    Client.Show()
    Client.Scan()
    app.MainLoop()