import os
import wx.xrc
import wx.richtext
import win32gui 
import win32con
import pyautogui as pag
from time import sleep
from threading import Thread

from mouse import click,drag
from image.Anchor_point_png import img as  Anchor_point_png
from image.confrim_normal_png import img as confrim_normal_png
from image.confrim_secrect_png import img as confrim_secrect_png
from image.normal2_png import img as normal2_png
from image.reset_confrim_png import img as reset_confrim_png
from image.reset_full_size_png import img as reset_full_size_png
from image.secrect2_png import img as secrect2_png


import base64
from io import BytesIO
from PIL import Image

titles = set()
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image")

stop_loop_btn = False
nortotal,secrettotal = 0,0


def transfer_byte_to_img(img_byte):
    byte_data = base64.b64decode(img_byte)
    image_data = BytesIO(byte_data)
    return Image.open(image_data)

def click_safe_out(clicktime):
  if clicktime>20:
    exit()

def buy_up(ls,str,Confirm_buy_point,Anchor_point_top):
  clicktime = 0
  while True:
    pag.moveTo(x=Anchor_point_top.x,y=ls+20,_pause = False)
    click()
    clicktime+=1
    click_safe_out(clicktime)
    sleep(0.8)
    y= pag.locateCenterOnScreen(transfer_byte_to_img(str))
    if(y == None):
      continue
    else:
      clicktime = 0
      while True:
        pag.moveTo(Confirm_buy_point.x,Confirm_buy_point.y,_pause = False)
        click()
        clicktime+=1
        click_safe_out(clicktime)
        sleep(0.8)
        if pag.locateCenterOnScreen(transfer_byte_to_img(str)) != None:
          continue
        break
      break
  
def buy_down(ls , total,str,Confirm_buy_point,Anchor_point_top):
  if ls > 600:
    clicktime = 0
    while True:
      pag.moveTo(x=Anchor_point_top.x,y=ls+20,_pause = False)
      click()
      clicktime+=1
      click_safe_out(clicktime)
      sleep(0.8)
      #pag.click(x=Anchor_point_top.x,y=ls+20)
      y= pag.locateCenterOnScreen(transfer_byte_to_img(str))
      if(y == None):
        continue
      else:
        clicktime = 0
        while True:
          pag.moveTo(Confirm_buy_point.x,Confirm_buy_point.y,_pause = False)
          click()
          clicktime+=1
          click_safe_out(clicktime)
          sleep(0.8)
          #pag.click(Confirm_buy_point.x,Confirm_buy_point.y)
          if pag.locateCenterOnScreen(transfer_byte_to_img(str)) != None:
            continue
          break
        break
    return total+1
  else:
    return total
  
def get_screen_Anchor_point():

  Anchor_point_down = pag.locateCenterOnScreen(transfer_byte_to_img(reset_full_size_png),confidence=0.7)
  Anchor_point_top = pag.locateCenterOnScreen(transfer_byte_to_img(Anchor_point_png),confidence=0.7)
  return Anchor_point_top,Anchor_point_down 

def main_loop(Scroll_point,Confirm_buy_point,Anchor_point_top,Anchor_point_down,nortotal,secrettotal):
    ls = pag.locateCenterOnScreen(transfer_byte_to_img(normal2_png),confidence=0.8)
    if(ls!= None):
      sleep(1)
      buy_up(ls.y,confrim_normal_png,Confirm_buy_point,Anchor_point_top)
      nortotal+=1
      sleep(1)
    
    ls = pag.locateCenterOnScreen(transfer_byte_to_img(secrect2_png),confidence=0.8)
    if(ls!= None):
      sleep(1)
      buy_up(ls.y,confrim_secrect_png,Confirm_buy_point,Anchor_point_top)
      secrettotal+=1
      sleep(1)

    sleep(1)
    drag(Scroll_point.x,Scroll_point.y,Scroll_point.x, Scroll_point.y-400,True,0.5)
    sleep(1)
    

    ls = pag.locateCenterOnScreen(transfer_byte_to_img(normal2_png),confidence=0.8)
    if(ls!= None):
      sleep(1)
      
      nortotal = buy_down(ls.y, nortotal,confrim_normal_png,Confirm_buy_point,Anchor_point_top)
      
    ls = pag.locateCenterOnScreen(transfer_byte_to_img(secrect2_png),confidence=0.8)
    if(ls!= None):
      sleep(1)
      secrettotal = buy_down(ls.y, secrettotal,confrim_secrect_png,Confirm_buy_point,Anchor_point_top)

    while True:
      sleep(0.5)
      pag.moveTo(Anchor_point_down.x,Anchor_point_down.y,_pause = False)
      click()

      sleep(0.4)
      if pag.locateCenterOnScreen(transfer_byte_to_img(reset_confrim_png),confidence=0.8) != None:
        while True:

          tmp = pag.locateCenterOnScreen(transfer_byte_to_img(reset_confrim_png),confidence=0.8)
          pag.moveTo(tmp.x,tmp.y,_pause = False)
          click()

          sleep(0.4)
          if pag.locateCenterOnScreen(transfer_byte_to_img(reset_confrim_png),confidence=0.8)== None:
            sleep(1)
            break
        break
      else:
        continue
    return nortotal,secrettotal

def foo(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        titles.add(win32gui.GetWindowText(hwnd))

class Check_Stop_Thread(Thread):
    def __init__(self, wxObject):
        Thread.__init__(self)
        self.wxObject = wxObject
        self.start()
    def run(self):
        output100 = self.wxObject.m_checkBox1.GetValue()
        Infinity_round = self.wxObject.m_checkBox11.GetValue()
        times = int(self.wxObject.m_textCtrl1.GetValue())
        Pause_time = 0.8
        global stop_loop_btn,nortotal,secrettotal

        
        sleep(2)
        
        nortotal,secrettotal = 0,0

        pag.PAUSE=Pause_time
        Anchor_point_top,Anchor_point_down  = get_screen_Anchor_point()
        Scroll_point = pag.Point(Anchor_point_down.x+(Anchor_point_top.x-Anchor_point_down.x)//4,Anchor_point_down.y)
        Confirm_buy_point = pag.Point(Anchor_point_down.x+(Anchor_point_top.x-Anchor_point_down.x)//2 , Anchor_point_top.y+3*(Anchor_point_down.y-Anchor_point_top.y)//4)
        
        if Infinity_round:
            total_times = 0
            while True:
                if not stop_loop_btn:
                    nortotal,secrettotal = main_loop(Scroll_point,Confirm_buy_point,Anchor_point_top,Anchor_point_down,nortotal,secrettotal)
                    if (total_times+1)%100 ==0 and output100:
                        self.wxObject.m_richText1.AppendText(f'聖約書簽:{nortotal}\n')
                        self.wxObject.m_richText1.AppendText(f'神秘書簽:{secrettotal}\n')
                else:
                    break
        else:
            for i in range(times):
                if not stop_loop_btn:
                    nortotal,secrettotal = main_loop(Scroll_point,Confirm_buy_point,Anchor_point_top,Anchor_point_down,nortotal,secrettotal)
                    if (i+1)%100 ==0 and output100:
                        self.wxObject.m_richText1.AppendText(f'聖約書簽:{nortotal}\n')
                        self.wxObject.m_richText1.AppendText(f'神秘書簽:{secrettotal}\n')
                else:
                    break
        
        #wx.PostEvent(self.wxObject, ResultEvent())

class ShopFrame ( wx.Frame ):
    def __init__( self, parent ):
        
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 471,250 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.stop_loop_btn = False
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Select your epic7 window", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText1.Wrap( -1 )
        
        self.m_staticText1.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "微軟正黑體" ) )

        bSizer5.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_choice2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 0 )
        bSizer5.Add( self.m_choice2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        
        bSizer4.Add( bSizer5, 0, wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"every 100 rounds output result", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體" ) )

        bSizer3.Add( self.m_staticText2, 0, wx.ALL, 5 )

        self.m_checkBox1 = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox1.SetValue(True)
        bSizer3.Add( self.m_checkBox1, 0, wx.ALL, 5 )
        
        bSizer4.Add( bSizer3, 0,wx.LEFT, 125 )

        bSizer31 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"INFINITY ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText21.Wrap( -1 )

        self.m_staticText21.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體" ) )

        bSizer31.Add( self.m_staticText21, 0, wx.ALL, 5 )

        self.m_checkBox11 = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer31.Add( self.m_checkBox11, 0, wx.ALL, 5 )


        bSizer4.Add( bSizer31, 0, wx.ALIGN_CENTER|wx.LEFT, 111 )

        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Times : ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        self.m_staticText5.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "微軟正黑體" ) )

        bSizer9.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, u"333", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.m_textCtrl1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_button1 = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.m_button1, 0, wx.ALL, 5 )
        bSizer4.Add( bSizer9, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_richText1 = wx.richtext.RichTextCtrl( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        
        self.bSizer6.Add( self.m_richText1, 1, wx.ALL|wx.EXPAND, 5 )

        

        bSizer4.Add( self.bSizer6, 1, wx.EXPAND, 5 )

        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        self.m_button2 = wx.Button( self, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.m_button2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        self.m_button2.Disable()

        bSizer4.Add( bSizer7, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
       
#bind event---------------------------
        self.m_button1.Bind( wx.EVT_BUTTON, self.OnBtnClickStart )
        self.m_button2.Bind( wx.EVT_BUTTON, self.OnBtnClickStop )
        self.m_checkBox11.Bind( wx.EVT_CHECKBOX, self.Inifity_check_click )
        self.Bind(wx.EVT_CLOSE, self.OnExit)
#-------------------------------------
        self.SetSizer( bSizer4 )
        self.Layout()

        self.Centre( wx.BOTH )
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #self.Connect(-1,-1,EVT_RESULT_ID,self.doloop)
        
    def OnBtnClickStop(self, event): 
        global stop_loop_btn,nortotal,secrettotal
        stop_loop_btn = True
        hwnd = win32gui.FindWindow(None, self.m_choice2.GetString(self.m_choice2.GetSelection()))
        #print(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP  , 0, 0, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        self.m_richText1.AppendText("Stop loop\n")
        self.m_richText1.AppendText(f'聖約書簽:{nortotal}\n')
        self.m_richText1.AppendText(f'神秘書簽:{secrettotal}\n')
        self.m_button1.Enable()

    def OnExit(self, event):

        self.Destroy()
    def __del__ (self):
        pass
    def Inifity_check_click( self, event):
        self.m_textCtrl1.Enable(not self.m_checkBox11.IsChecked())
            
    def OnBtnClickStart( self, event ):
        global stop_loop_btn
        stop_loop_btn = False

        hwnd = win32gui.FindWindow(None, self.m_choice2.GetString(self.m_choice2.GetSelection()))
        #print(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP  , 0, 0, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        #left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        #print(left, top, right, bottom)
        hwnd = win32gui.FindWindow(None, "Epic7 Auto shop")
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,win32con.SWP_NOMOVE  | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)

        Check_Stop_Thread(self)
        btn = event.GetEventObject()
        btn.Disable()
        self.m_button2.Enable()
        
        
if __name__ == '__main__':
    
    app = wx.App()
    frm = ShopFrame(None)
    frm.SetTitle("Epic7 Auto shop")
    frm.Show()
    win32gui.EnumWindows(foo, 0)
    m_choice2Choices = [t for t in titles if t]
    frm.m_choice2.Append(m_choice2Choices)
    hwnd = win32gui.FindWindow(None, "Epic7 Auto shop")
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 118, 251, 0, 0, win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
    app.MainLoop()
    
