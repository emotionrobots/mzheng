#!/usr/bin/python3
#========================================================================
#
#  vBeaconTest.py
#
#  Copyright (c) 2020-2021, E-Motion, Inc.
#
#  This SOFTWARE PRODUCT is provided "as-is". PROVIDER  makes no 
#  representations or warranties of any kind concerning the suitability 
#  and safety of the SOFTWARE PRODUCT for any applications.  Makers of 
#  products containing the SOFTWARE are solely responsible for the 
#  suitability and safety the product.  E-Motion will not be liable 
#  for any damages one may suffer in connection with using, modifying, 
#  or distributing this SOFTWARE PRODUCT.
#
#========================================================================
import sys
import time
sys.path.append('lib')
from PiSugar2 import PiSugar2
from ePaper import ePaper
from ui import UI, Color, TTFont
from vBeacon import vBeacon
from Buzzer import Buzzer

 

#========================================================================
#  myBeaconCallback
#========================================================================
def myBeaconCallback(major, minor, txPower, rssi):
  print(f"major={major}, minor={minor}, txPower={txPower}, rssi={rssi}")




#========================================================================
#  Customized UI 
#========================================================================
def beaconToggle(widget):
  global vbeacon
  print("beaconToggle({widget.cname}.{widget.id}) called")
  #print("DEBUG: "+(str)(vbeacon.isAdvertising))
  if vbeacon.isAdvertising:
    widget.text = " Beacon:\n Off"
    vbeacon.stopAdvertising()
    vbeacon.stopScanning()
    print("DEBUG: beacon turned off")
  else:
    widget.text = " Beacon:\n On"
    vbeacon.startAdvertising()
    vbeacon.startScanning()
    print("DEBUG: beacon turned on")

def displaySelect1(widget):
  global displayBoxItem
  print("displaySelect1({widget.cname}.{widget.id}) called")
  displayBoxItem = 1
  updateDisplayBox(displayBoxItem)

def displaySelect2(widget):
  global displayBoxItem
  print("displaySelect2({widget.cname}.{widget.id}) called")
  displayBoxItem = 2
  updateDisplayBox(displayBoxItem)

def displaySelect3(widget):
  global displayBoxItem
  print("displaySelect3({widget.cname}.{widget.id}) called")
  displayBoxItem = 3
  updateDisplayBox(displayBoxItem)
  
def updateDisplayBox(currentSelect):
  global qrpath, vbeacon, whiteRectPath, ui
  print("updateDisplayBox called:"+(str)(currentSelect))
  if currentSelect == 1:
    nearbyCount.text = ""
    nearbyCount.dim = [0,0]
    qrspace.file = qrpath
  elif currentSelect == 2:
    nearbyCount.text = str(len(vbeacon.getNearbyBeacons()))
    nearbyCount.dim = [95,95]
    qrspace.file = whiteRectPath
    ui.render()
  else:
    nearbyCount.text = ""
    qrspace.file = whiteRectPath
    #nearbyCount.dim = [0,0]


def buildCustomUI(ui):
  global vbeacon, qrpath, nearbyCount

  qrbox = ui.addRect(pos=[150,0], dim=[100,100], outline=Color.black, fill=Color.white)
  qrbox.isSelectable = False

  updateDisplayBox(1)

  

  #qrspace = ui.addImageBox(pos=[150,0], file=qrpath) 
  qrspace.isSelectable = False

  #nearbyCount = ui.addTextBox(pos=[180,30], dim=[25,25], text="10", font=TTFont(25), outline=Color.white, fill=Color.white)
  nearbyCount.isSelectable = False
  #nearbyCount.text = str(len(vbeacon.getNearbyBeacons()))
  

  #  Horizontal list box
  dropList = ui.addDropList(pos=[10,10], dim=[62, 20], text=" Option", font=TTFont(15), offset=[0,20],
                  textColor=Color.black, outline=Color.black, fill=Color.white)

  choice1 = dropList.addEntry(0, " Beacon:\n On")
  choice1.onSelect = beaconToggle

  choice1.dim = [60,40]
  
  dropList2 = ui.addDropList(pos=[72,10], dim=[62, 20], text=" Select", font=TTFont(15), offset=[0,20],
                  textColor=Color.black, outline=Color.black, fill=Color.white)
  select1 = dropList2.addEntry(0, " QR Code")
  select1.onSelect = displaySelect1
  select2 = dropList2.addEntry(1, " Nearby")
  select2.onSelect = displaySelect2
  select3 = dropList2.addEntry(2, " None")
  select3.onSelect = displaySelect3
  
  
  ticker = ui.addTickerTape(pos=[0, ui.display.height-25], dim=[2, 25], 
                  text="Go Astros!  Go Rockets!  Go Texasns!  Go Dynamos!  Go Houston!", 
                  font=TTFont(20),
                    textColor=Color.black, outline=Color.white, fill=Color.white)
  ticker.margin = [2, 2] 
  
  

  ui.firstFocusId = dropList.id
  return


#========================================================================
#
#  main
#
#========================================================================
def main(args):
  global pisugar,paper,ui
  buzzer = Buzzer(pin=16)

  buzzer.play(sound=buzzer.alert, blocking=False, repeat=100)

  ui.build = buildCustomUI
  ui.start()


  vbeacon.startScanning()    
  vbeacon.startAdvertising()    
  print("--------------------------\nDEBUG 1: "+(str)(vbeacon.isAdvertising)+"\n-----------------------")

  done = False
  while not done:
    try:
      beaconsNearby = vbeacon.getNearbyBeacons()
      
      print("-------------------------------------")
      print(f" {len(beaconsNearby)} beacons nearby")
      print("-------------------------------------")
      
      for beacon in beaconsNearby:
        print(f"{beacon}")

      
      time.sleep(1.0)
    except KeyboardInterrupt:
      done = True

  vbeacon.stopAdvertising()
  vbeacon.stopScanning()

#========================================================================
#
#  Variables declared here so UI functions have access to them
#
#========================================================================
vbeacon = vBeacon(uuid="2f234454-cf6d-4a0f-adf2-f4911ba9ffa6", 
                   major=2, minor=7777, txPower=-59, callback=myBeaconCallback, expiration=30)

pisugar = PiSugar2()
paper = ePaper()
ui = UI(paper, pisugar.get_button_press)

displayBoxItem = 1

qrpath = "/etc/PiBeacon/pics/emotionlogo.bmp"
qrspace = ui.addImageBox(pos=[150,0], file=qrpath)
whiteRectPath = "white100x100.bmp"

nearbyCount = ui.addTextBox(pos=[150,0], dim=[0,0], text="", font=TTFont(50), outline=Color.black, fill=Color.white)

if __name__ == '__main__':
  main(sys.argv[1:])
   

