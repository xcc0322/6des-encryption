## -*- coding: cp437 -*-
#----------------------------------------------------------------------------
# Name:         DES_GUI.py
# Purpose:      [PJ 1.1]An implementation for DES encryption and decryption.
#               6 times in CBC way.
#               GUI in wxPython.
# Author:       Chengcheng Xu
#
# Created:      2013.10.8
#----------------------------------------------------------------------------

import  random
import  wx
import  wx.lib.buttons  as  buttons
import  wx.lib.dialogs
import  wx.lib.filebrowsebutton as filebrowse
import  DES_Encryptor


class TestFrame(wx.Frame):
    def __init__(self):
        self.mode = "Encryption"
        wx.Frame.__init__(self, None, -1, "DES Impletation Project-11300240100")
        p = wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
                     | wx.CLIP_CHILDREN
                     | wx.FULL_REPAINT_ON_RESIZE
                     )
        # Headline
        gbs = self.gbs = wx.GridBagSizer(5, 5)
        headline = wx.StaticText(p, -1, "DES Cipher Machine")
        headline.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        gbs.Add(headline, (0,0), (1,10), wx.ALIGN_CENTER | wx.ALL, 5)
        
        # Mode Choice
        mode_choice = wx.RadioBox(p, -1, "Encryption or Decryption", wx.DefaultPosition,
            wx.DefaultSize, ["Encryption", "Decryption"], 2, wx.RA_SPECIFY_ROWS)
        gbs.Add( mode_choice, (1,0), (1,10), wx.ALIGN_CENTER)
        self.Bind(wx.EVT_RADIOBOX, self.ModeChoice, mode_choice)

        # Key
        label = wx.StaticText(p, -1, "Input 64-bit Key:")
        label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False))
        gbs.Add(label, (2,0), (1,10), wx.ALIGN_CENTER | wx.ALL, 5)
        self.keys = []
        for i in range(8):
          self.keys.append(wx.TextCtrl(p, -1, self.RandomBinaryGenerate(8)))
          gbs.Add( self.keys[i], (3+i/4, (i%4+1)*2-1) )
          if i%4!=3:
            gbs.Add( wx.StaticText(p, -1, "-"), (3+i/4, (i%4+1)*2) )
              
        # Source File
        label = wx.StaticText(p, -1, "Choose Source File:")
        label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False))
        gbs.Add(label, (5,0), (1,10), wx.ALIGN_CENTER | wx.ALL, 5)
        file_choice = filebrowse.FileBrowseButton(
            p, -1, size=(350, -1),
            changeCallback = self.FileBrowseButtonCallback,
            labelText=""
        )
        gbs.Add( file_choice, (6,0), (1,10), wx.ALIGN_CENTER | wx.ALL, 5)

        # Execute Button
        execute_button = buttons.GenButton(p, -1, "Do it")
        execute_button.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD, False))
        
        execute_button.SetBackgroundColour("Navy")
        execute_button.SetForegroundColour(wx.WHITE)
        execute_button.SetBezelWidth(5)
        gbs.Add( execute_button, (8,0), (1, 10), wx.ALIGN_CENTER | wx.ALL)
        self.Bind(wx.EVT_BUTTON, self.OnButton, execute_button)

        # End
        box = wx.BoxSizer()
        box.Add(gbs, 0, wx.ALL, 10)
        p.SetSizerAndFit(box)
        self.SetClientSize(p.GetSize())

    def RandomBinaryGenerate(self, l):
        return ''.join("0" if random.random() < 0.5 else "1" for i in range(l))

    def ModeChoice(self, event):
        self.mode = event.GetString()
        print self.mode

    def FileBrowseButtonCallback(self, evt):
        self.file = evt.GetString()
        print 'FileBrowseButton: %s\n' % evt.GetString()
        
    def OnButton(self, evt):
        key_string = "".join([k.Value for k in self.keys])
        print "key_string(%d):\n %s" % (len(key_string), key_string)
        f = open(self.file, "r")
        input_string = f.read()
        f.close()
        print "key_string(%d):\n %s" % (len(key_string), key_string)

        dept = DES_Encryptor.DesEncryptor(key_string)
        if self.mode == "Encryption":
            output_string = dept.Encrypt(input_string)
        else:
            output_string = dept.Decrypt(input_string)
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, output_string, " Result")
        dlg.ShowModal()

    def DesEncrypt(self, key_string, input_string):
        return key_string
        

class MyApp(wx.App):
    def OnInit(self):
        frame = TestFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()
