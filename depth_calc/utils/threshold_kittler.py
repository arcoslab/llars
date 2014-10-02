#!/usr/bin/python

from math import pi as PI
from math import log as log
from PIL import Image

gray = Image.open('imagenes/gray_3.jpg')
#gray = imagen.convert("L")

vmax =-9888888888888888888888.0
Vth=-8888888888888888888888.0
th0=0
M1o = 0.0
M2o = 0.0
sigma1o = 0.0
sigma2o = 0.0

width, height = gray.size
size_image = width*height
histo = gray.histogram()

min_value, max_value = gray.getextrema()
th1 = 3*(max_value - min_value)/4.
print th1

probabilidades = []
for i in range(len(histo)):
	p = histo[i]/(size_image*1.0)
	probabilidades.append(p)

for th in range(256):
	C1=0.0
	C2=0.0
	m1=0.0
	m2=0.0
	sigma1 = 0.0
	sigma2 = 0.0
	
	for x in range(th+1):
		C1 = C1 + probabilidades[x]
	
	for y in range(th+1,256):
		C2 = C2 + probabilidades[y]	
	
	if(C1>0.00001 and C2>0.00001):
		for x in range(th+1):
			m1 = m1 + (x*probabilidades[x])/(C1*1.0)
	
		for y in range(th+1,256):
			m2 = m2 + (y*probabilidades[y])/(C2*1.0)
	
	
		for x in range(th+1):
			sigma1 = sigma1 + ((x-m1)**2) *(probabilidades[x])/(C1*1.0)

		for y in range(th+1,256):
			sigma2 = sigma2 + ((y-m2)**2) *(probabilidades[y])/(C2*1.0)

		
		if(sigma1>0.00001 and sigma2 > 0.00001):
			Vth = (size_image * (C1 * log(C1) + C2 * log(C2))) - ((size_image/(2.0))*log(2*PI)) - (size_image/(2.0))*(C1*log(sigma1) + C2*log(sigma2)) - (size_image/(2.0))
			if(Vth>vmax):
				vmax=Vth
				th0=th
				M1o = m1
				M2o = m2
				sigma1o = sigma1
				sigma2o = sigma2
					
print "Threshold th0:",th0
print "Mean 1:",M1o
print "Mean 2:",M2o
print "Variance 1:",sigma1o
print "Variance 2:",sigma2o



b_w = gray.copy()
image_pixel = b_w.load()	
width, height = b_w.size	
for h in range(height):
	for w in range(width):
		pixel = image_pixel[w,h]
		if pixel < th1:
			image_pixel[w,h]= 255
		elif pixel >= th1:
			image_pixel[w,h]= 0

b_w.show()


b_w1 = gray.copy()
image_pixel = b_w1.load()	
width, height = b_w.size	
for h in range(height):
	for w in range(width):
		pixel = image_pixel[w,h]
		if pixel < th0:
			image_pixel[w,h]= 255
		elif pixel >= th0:
			image_pixel[w,h]= 0
b_w1.show()

			
			
			
			
			
			
