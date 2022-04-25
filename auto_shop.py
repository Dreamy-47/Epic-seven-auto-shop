
import json
import os

import pyautogui as pag
from time import sleep


image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image")
Anchor_point_top,Anchor_point_down = 0,0
Confirm_buy_point =0
def buy_up(ls):
  pag.click(x=Anchor_point_top.x,y=ls+20)
  pag.click(Confirm_buy_point.x,Confirm_buy_point.y)
  
def buy_down(ls , total):
  if ls > 600:
    pag.click(x=Anchor_point_top.x,y=ls+20)
    pag.click(Confirm_buy_point.x,Confirm_buy_point.y)
    return total+1
  else:
    return total
  
def get_screen_Anchor_point():

  Anchor_point_down = pag.locateCenterOnScreen(os.path.join(image_path,'reset_full_size.png'),confidence=0.7)
  Anchor_point_top = pag.locateCenterOnScreen(os.path.join(image_path,'Anchor_point.png'),confidence=0.7)
  return Anchor_point_top,Anchor_point_down 

def main(cfg):
  global Anchor_point_top,Anchor_point_down,Confirm_buy_point
  sleep(2)
  
  nortotal,secrettotal = 0,0
  pag.PAUSE=0.5
  
  Anchor_point_top,Anchor_point_down  = get_screen_Anchor_point()
  Scroll_point = pag.Point(Anchor_point_down.x+(Anchor_point_top.x-Anchor_point_down.x)//4,Anchor_point_down.y)
  Confirm_buy_point = pag.Point(Anchor_point_down.x+(Anchor_point_top.x-Anchor_point_down.x)//2 , Anchor_point_top.y+3*(Anchor_point_down.y-Anchor_point_top.y)//4)
  
  if Anchor_point_top == None or Anchor_point_down == None:
    print("Can't get Anchor_point")
    print("Anchor_point_down is:"+str(Anchor_point_down))
    print("Anchor_point_top is:"+str(Anchor_point_top))
    exit()
  print("Anchor_point_down is:"+str(Anchor_point_down))
  print("Anchor_point_top is:"+str(Anchor_point_top))
  print("Scroll_point is:"+str(Scroll_point))
  print("Confirm_buy_point is:"+str(Confirm_buy_point))
  
  
  for i in range(cfg['times']):
    ls = pag.locateCenterOnScreen(os.path.join(image_path,'normal2.png'),confidence=0.8)
    if(ls!= None):
      buy_up(ls.y)
      nortotal+=1
      sleep(1)
    
    ls = pag.locateCenterOnScreen(os.path.join(image_path,'secrect2.png'),confidence=0.8)
    if(ls!= None):
      buy_up(ls.y)
      secrettotal+=1
      sleep(1)
    
    pag.moveTo(Scroll_point.x,Scroll_point.y)
    pag.dragTo(Scroll_point.x, Scroll_point.y-400, 0.5, button='left')

    ls = pag.locateCenterOnScreen(os.path.join(image_path,'normal2.png'),confidence=0.8)
    if(ls!= None):
      sleep(1)
      
      nortotal = buy_down(ls.y, nortotal)
      
    ls = pag.locateCenterOnScreen(os.path.join(image_path,'secrect2.png'),confidence=0.8)
    if(ls!= None):
      sleep(1)
      secrettotal = buy_down(ls.y, secrettotal)

    if (nortotal>=10) and (cfg['stop_when_get_ten'] == True):
      break

    while True:
      sleep(0.5)
      pag.click(Anchor_point_down)
      sleep(0.4)
      if pag.locateCenterOnScreen(os.path.join(image_path,'reset_confrim.png'),confidence=0.8) != None:
        while True:
          pag.click(pag.locateCenterOnScreen(os.path.join(image_path,'reset_confrim.png'),confidence=0.8))
          sleep(0.4)
          if pag.locateCenterOnScreen(os.path.join(image_path,'reset_confrim.png'),confidence=0.8)== None:
            break
        break
      else:
        continue

  if cfg['showoutput']:
    print('聖約書簽:',nortotal)
    print('神秘書簽:',secrettotal)

if __name__ == "__main__":
  with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json') , 'r',encoding="utf8") as f:
        cfg = json.load(f)
  
  main(cfg)