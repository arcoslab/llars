from PIL import Image
from PIL import ImageFilter
import numpy as np
import cv2
import datetime
import os
import time
import math
import matplotlib.pyplot as plt


#Metodo para guardar los datos
def write2file(hola, nombre):
	if type(hola) == list:
		f = open("Datos_pruebas/" + nombre +".txt", "w")
		for i in hola:
			f.write(str(i))
			f.write('\n')
				
	#	f.writelines(["%s\n" % item  for item in hola])
		f.close()



i=1
while(i<2):
	#os.system('uvccapture -d/dev/video1 -x1280 -y720')
	#os.system('uvccapture -m')
	imagen = Image.open('snap.jpg')
	gray = imagen.convert("L")


	width, height = gray.size
	b_w = gray.crop((0, 5*height/11, width, (6*height/11)))
#	b_w = gray.copy()
	b_w.show()
	
	min_value, max_value = b_w.getextrema()
	th = 3*(max_value - min_value)/4.

	b_w1 = []
	width, height = b_w.size
	image_pixel = b_w.load()
	for h in range(height):
		for w in range(width):
			
			if image_pixel[w,h] <= th:
				image_pixel[w,h] = 0 #blanco
				
			else:
				image_pixel[w,h] = 1 #negro
			
			b_w1.append(image_pixel[w,h])
	
	write2file(b_w1, "b_w1")	
	#os.system('gedit Datos_pruebas/b_w1.txt &')
	
	b_w.show("0y1")
	
	v = []
	label = 2
	equivalencias = [0]*500
	image_pixel = b_w.load()
	for h in range(height):
		for w in range(width):

			if (w == 0 or h == 0 or w == (width-1)):
				pass
						
			else:
				#si no es blanco
				if image_pixel[w,h] != 0:
					vecinos = []				
					if image_pixel[w-1,h] != 0:
						vecinos.append(image_pixel[w-1,h])
					if image_pixel[w,h-1] != 0:
						vecinos.append(image_pixel[w,h-1])
					if 	image_pixel[w-1,h-1] != 0:
						vecinos.append(image_pixel[w-1,h-1])
					if image_pixel[w+1,h-1] != 0:
						vecinos.append(image_pixel[w+1,h-1])
		
#					print vecinos
					
					v.append(vecinos)
					
					if not vecinos:
						image_pixel[w,h] = label
						label += 1
					
					  
					else:				  
						min_equivalencia = min(vecinos)
						max_equivalencia = max(vecinos)
						image_pixel[w,h] = min_equivalencia
						
						for i in range(len(vecinos)):
							if (equivalencias[vecinos[i]] == 0 or equivalencias[vecinos[i]] > min_equivalencia):
								equivalencias[vecinos[i]] = min_equivalencia

	write2file(equivalencias,"equivalencias")
	
	for h in range(height):
		for w in range(width):
			#if equivalencias[image_pixel[w,h]] != 0:		
			image_pixel[w,h] = equivalencias[image_pixel[w,h]]
	
	b_w.show()
	write2file(v,'v')
	write2file(equivalencias,"equivalencias")	
	b_w.save("b_w.jpg")
	#os.system('geeqie b_w.jpg &')
	i+=1
	#raw_input("Press Enter to continue...")
	



