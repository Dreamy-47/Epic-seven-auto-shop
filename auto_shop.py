import json
import os
import pyautogui
from time import sleep
def buy_up(ls):
  if(ls<300):
    pyautogui.press('num1')
    pyautogui.press('num9')
  elif(ls<500):
    pyautogui.press('num2')
    pyautogui.press('num9')
  elif(ls<700):
    pyautogui.press('num3')
    pyautogui.press('num9')
  elif(ls<900):
    pyautogui.press('num4')
    pyautogui.press('num9')

def buy_down(ls):
  if(ls<800 and ls>600):
    pyautogui.press('num5')
    pyautogui.press('num9')
  elif(ls<1000 and ls>800):
    pyautogui.press('num6')
    pyautogui.press('num9')

def main(jdata):
  sleep(2)
  

  image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image")
  
  pyautogui.PAUSE=0.5
  nortotal,secrettotal = 0,0
  for i in range(jdata['times']):
    ls = pyautogui.locateCenterOnScreen(os.path.join(image_path,'normal2.png'),confidence=0.8)
    if(ls!= None):
      buy_up(ls.y)
      nortotal+=1
      print(1)
      sleep(1)
    ls = pyautogui.locateCenterOnScreen(os.path.join(image_path,'secrect2.png'),confidence=0.8)
    if(ls!= None):
      buy_up(ls.y)
      secrettotal+=1
      sleep(1)
    pyautogui.moveTo(700, 800)
    pyautogui.dragTo(700, 400, 0.5, button='left')
    ls = pyautogui.locateCenterOnScreen(os.path.join(image_path,'normal2.png'),confidence=0.8)
    if(ls!= None):
      sleep(1)
      buy_down(ls.y)
      nortotal+=1
      print(2)
    ls = pyautogui.locateCenterOnScreen(os.path.join(image_path,'secrect2.png'),confidence=0.8)
    if(ls!= None):
      sleep(1)
      buy_down(ls.y)
      secrettotal+=1
    if nortotal>=10:
      break
    pyautogui.press('ctrlleft')
    pyautogui.press('num8')
    sleep(1)

  if jdata['showoutput']:
    print(nortotal)
    print(secrettotal)

if __name__ == "__main__":
  with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json') , 'r',encoding="utf8") as jfile:
          jdata = json.load(jfile)
  
  main(jdata)