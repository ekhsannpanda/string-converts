import wx
import re
from pathlib import Path

# App
_app = wx.App()

# Const
_fileDir = Path

# UI
_window = wx.Frame(None, title = "String File Convert", size = (300,500)) 
_panel = wx.Panel(_window) 
wx.StaticText(_panel, label = "Select File (ONLY .txt/.xml)", pos = (20,10))
_selectBtn = wx.Button(_panel,label = "Select", pos = (20,30))
_selectLbl = wx.StaticText(_panel, label = "No File Selected", pos = (20,50))
wx.StaticText(_panel, label = "Select process conversion process", pos = (20,100))
_selectProcess1 = wx.Button(_panel,label = "Export to Android", pos = (20,120))
_selectProcess2 = wx.Button(_panel,label = "Android to Export", pos = (20,120))
_selectProcess3 = wx.Button(_panel,label = "Android to iOS", pos = (20,150))
_selectLblProcess = wx.StaticText(_panel, label = "Processing...", pos = (20,180))
_selectLblComplete = wx.StaticText(_panel, label = "Completed!", pos = (20,200))

_selectProcess1.Hide()
_selectProcess2.Hide()
_selectProcess3.Hide()
_selectLblProcess.Hide()
_selectLblComplete.Hide()

# Func
def openFile(self):
    with wx.FileDialog(_window, "Open file",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as _fileDialog:
         if _fileDialog.ShowModal() == wx.ID_CANCEL:
            return 

        # Proceed loading the file chosen by the user
         global _fileDir
         _fileDir = Path(_fileDialog.GetPath())
         _selectProcess1.Hide()
         _selectProcess2.Hide()
         _selectProcess3.Hide()
         _selectLblProcess.Hide()
         _selectLblComplete.Hide()

         try:
            if _fileDir.suffix == '.xml':
               _selectLbl.SetLabel(_fileDir.stem+_fileDir.suffix)
               _selectProcess2.Show()
               _selectProcess3.Show()
               return
            elif _fileDir.suffix == '.txt':
               _selectProcess1.Show()
            else:
               _selectLbl.SetLabel("Invalid file format...")
               _selectProcess1.Hide()
               _selectProcess2.Hide()
               _selectProcess3.Hide()
               return
         except IOError:
            _selectLbl.SetLabel("Cannot open file '%s'.")
            return

def AndToExp(self):
   _oldLinesArray = list()
   _selectLblProcess.Show()
   _selectLblComplete.Hide()

   # read old file
   old = open(str(_fileDir), "r")
   for lines in old:
       _oldLinesArray.append(lines)
   old.close
   _selectLblProcess.SetLabel("Processing......")

   # modify content
   for i,lines in  enumerate(_oldLinesArray):
      _lines = lines
      _lines = _lines.replace('<!-- ', "<!--")
      _lines = _lines.replace('<!--', "//")
      _lines = _lines.replace(' -->', "-->")
      _lines = _lines.replace('-->', "")
      _lines = _lines.replace('<string name="', "")
      _lines = _lines.replace('">',"^")
      _lines = _lines.replace('</string>',"")
      _lines = _lines.replace('&#8230;', '...')
      _lines = _lines.replace('&amp;','&')
      _lines = _lines.replace('\\u2022','•')
      _oldLinesArray[i] = _lines
   
   # write in new file
   _selectLblProcess.SetLabel("Processing.........")
   _newDir = f"{_fileDir.stem}_export.txt"
   new = open(_newDir, "x")
   new.close
   new = open(_newDir, "a")
   for lines in _oldLinesArray:
      new.write(lines)
   new.close
   _selectLblComplete.Show()
   return

def ExpToAnd(self):
   _oldLinesArray = list()
   _selectLblProcess.Show()
   _selectLblComplete.Hide()

   # read old file
   old = open(str(_fileDir), "r")
   for lines in old:
       _oldLinesArray.append(lines)
   old.close
   _selectLblProcess.SetLabel("Processing......")

   # modify content
   for i,lines in  enumerate(_oldLinesArray):
      _lines = lines

      if "\n" == _lines[0]:
         _lines = _lines
      elif "\n" == _lines[len(_lines)-1]:
         index = len(_lines)-1
         _lines = _lines[:index] + _lines[index:].replace(_lines[index] , "", 1)

         if "//" in _lines:
            _lines = _lines.replace('//', "<!-- ")
            _lines += " -->\n"
            _lines = _lines.replace('	','')
         else:
            _lines = '<string name="'+_lines
            _lines += "</string>\n"
            _lines = _lines.replace('	','">')
      else:
            _lines = '<string name="'+_lines
            _lines += "</string>\n"
            _lines = _lines.replace('	','">')
      
      _lines = _lines.replace('•','\\u2022')
      _lines = _lines.replace('&', '&amp;')
      _lines = _lines.replace('...', '&#8230;')
      _lines = _lines.replace('<string name=""></string>','')
      _oldLinesArray[i] = _lines

   # write in new file
   _selectLblProcess.SetLabel("Processing.........")
   _newDir = f"{_fileDir.stem}_xml.txt"
   new = open(_newDir, "x")
   new.close
   new = open(_newDir, "a")
   for lines in _oldLinesArray:
      new.write(lines)
   new.close

   # rename extention
   path = Path(_newDir)
   path.rename(path.with_suffix('.xml'))
   _selectLblComplete.Show()
   return

def AndToiOS(self):
   _oldLinesArray = list()
   _selectLblProcess.Show()
   _selectLblComplete.Hide()

   # read old file
   old = open(str(_fileDir), "r")
   for lines in old:
       _oldLinesArray.append(lines)
   old.close
   _selectLblProcess.SetLabel("Processing......")

   # modify content
   for i,lines in  enumerate(_oldLinesArray):
      _lines = lines
      
      _lines = _lines.replace('<!-- ', "<!--")
      _lines = _lines.replace(' -->', "-->")
      _lines = _lines.replace('<!--', "//MARK: ")
      _lines = _lines.replace('-->', "")
      _lines = _lines.replace('<string name=', "")
      _lines = _lines.replace('</string>', '";')
      _lines = _lines.replace('">', '" = "')
      _lines = _lines.replace('&#8230;', '...')
      _lines = _lines.replace('&amp;','&')
      _lines = _lines.replace('\\u2022','•')
      _lines = _lines.replace('%s','%@')
      _oldLinesArray[i] = _lines

   # write in new file
   _selectLblProcess.SetLabel("Processing.........")
   _newDir = f"{_fileDir.stem}_ios.txt"
   new = open(_newDir, "x")
   new.close
   new = open(_newDir, "a")
   for lines in _oldLinesArray:
      new.write(lines)
   new.close

   # rename extention
   path = Path(_newDir)
   path.rename(path.with_suffix('.strings'))
   _selectLblComplete.Show()
   return

# onClick
_selectBtn.Bind(wx.EVT_LEFT_UP, openFile )
_selectProcess1.Bind(wx.EVT_LEFT_UP, ExpToAnd )
_selectProcess2.Bind(wx.EVT_LEFT_UP, AndToExp )
_selectProcess3.Bind(wx.EVT_LEFT_UP, AndToiOS )

# App
_window.Show(True) 
_app.MainLoop()