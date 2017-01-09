import serial
import time

class UART:

   def __init__(self, dev='/dev/ttyACM0', baud=115200):
      try:
         self.comm = serial.Serial(port=dev, baudrate=baud)
      except:
         exit("Serial port opening error")
   
   def read(self, color=None):
      if(color is None):
         self.comm.write('a')
         out=" "
         while out[len(out)-1] is not '*' and len(out) < 50:
            out += self.comm.read(1)
         if out[1] is '@' and out[len(out)-1] is "*":
             line = out.translate(None, '@* ')
             return line.split('\t')
         else:
            return False
            