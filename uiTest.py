from ui import UI, Color, TTFont
from ePaper import ePaper
from PiSugar2 import PiSugar2
import time

def build(self):
    dropList1 = self.addDropList(pos=(0,0), dim=(60, 25), text="Publish", font=TTFont(15), 
                    textColor=Color.black, outline=Color.black, fill=Color.white)
    publish1 = dropList1.addEntry(0, "On")

    dropList2 = self.addDropList(pos=(0,50), dim=(60, 25), text="Scan", font=TTFont(15), 
                    textColor=Color.black, outline=Color.black, fill=Color.white)
    scan1 = dropList2.addEntry(0, "On")

    dropList3 = self.addDropList(pos=(70,0), dim=(60, 25), text="Update & News", font=TTFont(15), 
                    textColor=Color.black, outline=Color.black, fill=Color.white)
    update1 = dropList3.addEntry(0, "On")

    dropList4 = self.addDropList(pos=(70,50), dim=(60, 25), text="QR Code", font=TTFont(15), 
                    textColor=Color.black, outline=Color.black, fill=Color.white)
    qr1 = dropList4.addEntry(0, "QR Code")
    qr2 = dropList4.addEntry(1, "Nearby #")
    qr3 = dropList4.addEntry(2, "Off")

    self.firstFocusId = dropList1.id
    return

def main():
  UI.build = build
  pisugar = PiSugar2()
  paper = ePaper()
  ui = UI(paper, pisugar.get_button_press)
  print(f"UI dimension (WxH) = {ui.dim[0]}x{ui.dim[1]}")
  ui.start()

  while not ui.exitLoop:
    time.sleep(1.0)
 
if __name__=='__main__':
  main()