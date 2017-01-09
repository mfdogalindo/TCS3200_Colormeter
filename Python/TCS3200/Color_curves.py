import TCS3200
import time
import turtle
import matplotlib.pyplot as plt
import numpy

COLOR_STeP = 0x0F
FILTER_SAMPLES = 2
DARKNESS_LIMIT = 560000

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
      red += negative_to_zero(DARKNESS_LIMIT-float(data[1]))
      green += negative_to_zero(DARKNESS_LIMIT-float(data[3]))
      blue += negative_to_zero(DARKNESS_LIMIT-float(data[5]))
      clear += negative_to_zero(DARKNESS_LIMIT-float(data[7])) 

   red = red/samples
   green = green/samples
   blue = blue/samples
   clear = clear/samples

   return [red,green,blue,clear]

#--------------------- GRAYSCALE SAMPLING ----------------------

grayscale_data = []
grayscale_samples = []

for color in range (0, 0x100, COLOR_STeP):
   html_color = "#"+'%06x' % (color | color << 8 | color << 16) 
   win.bgcolor(html_color)
   grayscale_samples += [color]
   grayscale_data += [get_filtred_sample(FILTER_SAMPLES)]


#--------------------- RED COLOR SAMPLING ----------------------
red_data = []  
red_samples = []
 
for level in range(0, 0x100, COLOR_STeP):
   html_color = "#"+'%06x' % (level << 16) 
   win.bgcolor(html_color)
   red_samples += [level]
   red_data += [get_filtred_sample(FILTER_SAMPLES)]

#--------------------- GREEN COLOR SAMPLING ---------------------
green_data = []   
green_samples = []

for level in range(0, 0x100, COLOR_STeP):
   html_color = "#"+'%06x' % (level << 8) 
   win.bgcolor(html_color)
   green_samples += [level]
   green_data += [get_filtred_sample(FILTER_SAMPLES)]



#--------------------- BLUE COLOR SAMPLING ----------------------
blue_data = []   
blue_samples = [] 

for level in range(0, 0x100, COLOR_STeP):
   html_color = "#"+'%06x' % (level) 
   win.bgcolor(html_color)
   blue_samples += [level]
   blue_data += [get_filtred_sample(FILTER_SAMPLES)]

#------------------------- PLOTTING --------------------------
consolidated_red=[]
consolidated_green=[]
consolidated_blue=[]
consolidated_clear=[]
minimal = []
maximum = []

plt.figure("RAW DATA")

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
     

   for x in range (0,len(samples)):
      red += [data[x][0]]
      green += [data[x][1]]
      blue += [data[x][2]]
      clear += [data[x][3]]


   if figure_num is 0:
      consolidated_clear = clear
      minimal += [min(clear)]
      maximum += [max(clear)] 
   if figure_num is 1:
      consolidated_red = red
      minimal += [min(red)]
      maximum += [max(red)]   
   if figure_num is 1:
      consolidated_red = red
      minimal += [min(red)]
      maximum += [max(red)]
   if figure_num is 2:
      consolidated_green = green
      minimal += [min(green)]
      maximum += [max(green)]
   if figure_num is 3:
      consolidated_blue = blue
      minimal += [min(blue)]
      maximum += [max(blue)]

   plt.subplot(2,2,figure_num+1)
   plt.title(title)
   plt.plot(samples,red,'r',samples,green,'g',samples,blue,'b',samples,clear,'b--')
   plt.xlim(0,0xFF)
   plt.gcf().autofmt_xdate()

#---------------------- NORMALIZED PLOT ------------------------
   
max=max(maximum)
min=min(minimal)


consolidated_red = (numpy.asarray(consolidated_red))/max
consolidated_green = (numpy.asarray(consolidated_green))/max
consolidated_blue =  (numpy.asarray(consolidated_blue))/max   
consolidated_clear =  (numpy.asarray(consolidated_clear))/max 


plt.figure("NORMALIZED")  
plt.plot(samples,consolidated_red,'r',samples,consolidated_green,'g',samples,consolidated_blue,'b',consolidated_clear,'c--')
plt.xlim(0,0xFF)
plt.gcf().autofmt_xdate() 

plt.show()




