#!/usr/bin/python

from PIL import Image
import os, sys

#Aqui enciende el laser

os.system('uvccapture -m')
imagen = Image.open('snap.jpg')
gray = imagen.convert("L")
gray.show()

#Aqui tengo q apagar el laser

os.system('uvccapture -m')
imagen2 = Image.open('snap.jpg')
gray2 = imagen2.convert("L")
image_pixel2 = gray2.load()
gray2.show()


b_w = gray.copy()
width, height = b_w.size
image_pixel = b_w.load()
for h in range(height):
	for w in range(width):
		
		image_pixel[w,h] = image_pixel[w,h] - image_pixel2[w,h]
b_w.show()
		
min_value, max_value = b_w.getextrema()
th = 3*(max_value - min_value)/4.0
print "Threshold: " , th

print max_value	

for h in range(height):
	for w in range(width):
		if image_pixel[w,h] == max_value:
			print w,h
			image_pixel[w,h] = 0





