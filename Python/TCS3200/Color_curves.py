import TCS3200
import time
import turtle
import matplotlib.pyplot as plt

COLOR_STeP = 0x0F
FILTER_SAMPLES = 2
SENSOR_OFFSET = 50000


Colormeter = TCS3200.UART('/dev/ttyACM0',115200)


win = turtle.Screen()
win.setup(600,600)
win.title("Color meter RGB test")
win.bgcolor("black")


time.sleep(0.5)

def negative_to_zero(value):
   return (abs(value)+value)/2 

def get_filtred_sample(samples):
   red=0
   green=0
   blue=0
   clear=0
   for x in range (0,samples):
      data = Colormeter.read()
      red += negative_to_zero(SENSOR_OFFSET-float(data[1]))
      green += negative_to_zero(SENSOR_OFFSET-float(data[3]))
      blue += negative_to_zero(SENSOR_OFFSET-float(data[5]))
      clear += negative_to_zero(SENSOR_OFFSET-float(data[7]))  
   return [(red/samples),(green/samples),(blue/samples),(clear/samples)]

#--------------------- GRAYSCALE SAMPLING ----------------------

grayscale_data = []
counter =0

for color in range (0, 0x100, COLOR_STeP):
   html_color = "#"+'%06x' % (color | color << 8 | color << 16) 
   win.bgcolor(html_color)
   counter+=1
   grayscale_data += [get_filtred_sample(FILTER_SAMPLES)]

grayscale_samples = [i for i in range(counter)]

#--------------------- RED COLOR SAMPLING ----------------------
red_data = []   
counter = 0   

for level in range(0, 0x100, COLOR_STeP):
   html_color = "#"+'%06x' % (level << 16) 
   win.bgcolor(html_color)
   counter+=1
   red_data += [get_filtred_sample(FILTER_SAMPLES)]

red_samples = [i for i in range(counter)]  

#--------------------- GREEN COLOR SAMPLING ---------------------
green_data = []   
counter = 0   

for level in range(0, 0x100, COLOR_STeP):
   html_color = "#"+'%06x' % (level << 8) 
   win.bgcolor(html_color)
   counter+=1
   green_data += [get_filtred_sample(FILTER_SAMPLES)]

green_samples = [i for i in range(counter)]  

#--------------------- BLUE COLOR SAMPLING ----------------------
blue_data = []   
counter = 0   

for level in range(0, 0x100, COLOR_STeP):
   html_color = "#"+'%06x' % (level) 
   win.bgcolor(html_color)
   counter+=1
   blue_data += [get_filtred_sample(FILTER_SAMPLES)]

blue_samples = [i for i in range(counter)]  

#------------------------- PLOTTING --------------------------
consolidated_red=[]
consolidated_green=[]
consolidated_blue=[]

plt.figure(1)

for figure_num in range (0,4):
   data=[]
   samples = []
   red=[]
   green=[]
   blue=[]
   clear=[]
   title=""
   
   if figure_num is 0:
      samples = grayscale_samples
      data = grayscale_data
      title = "Grayscale"
   if figure_num is 1:
      samples = red_samples
      data = red_data
      title = "Red"
   if figure_num is 2:
      samples = green_samples
      data = green_data
      title = "Green"
   if figure_num is 3:
      samples = blue_samples
      data = blue_data   
      title = "Blue"
     

   for x in samples:
      red += [data[x][0]]
      green += [data[x][1]]
      blue += [data[x][2]]
      clear += [data[x][3]]
   
   if figure_num is 1:
      consolidated_red = red
   if figure_num is 2:
      consolidated_green = green
   if figure_num is 3:
      consolidated_blue = blue

   plt.subplot(2,2,figure_num+1)
   plt.title(title)
   plt.plot(samples,red,'r',samples,green,'g',samples,blue,'b',samples,clear,'b--')
   plt.gcf().autofmt_xdate()

plt.figure(2)  
plt.title("Consolidated")
plt.plot(samples,consolidated_red,'r',samples,consolidated_green,'g',samples,consolidated_blue,'b')
plt.gcf().autofmt_xdate() 

plt.show()




