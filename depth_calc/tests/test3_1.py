#!/usr/bin/python

#""""
#test3.py gets the coordenate of a laser in an image
#author: Carolina Arauz Villegas
#2013

#""""

#####################################################
#Importar librerias
#####################################################

from PIL import Image
from PIL import ImageFilter
import numpy as np
import cv2
import datetime
import os
import time
import math
import matplotlib.pyplot as plt

###################################################################
#Metodo para guardar un archivo y una imagen
###################################################################

#Metodo para guardar los datos
def write2file(hola, nombre):
	if type(hola) == list:
		f = open("Datos_pruebas/" + nombre +"." + datetime.datetime.now().ctime()+ ".txt", "w")
		for i in hola:
			f.write(str(i))
			f.write('\n')
				
	#	f.writelines(["%s\n" % item  for item in hola])
		f.close()


#for inner_list in listoflists:
#    for element in inner_list:
#        f.write(element+'\n')

#f.close()
#Metodo para guardar las imagenes
def save_image(imagen, nombre):
		imagen.save("Imagenes_pruebas/"+ nombre +"." + datetime.datetime.now().ctime() +".jpg")

#######################################################
#Capturar la imagen y convertirla a escala de grises
#######################################################
def open_convert(filename):
	imagen = Image.open(filename)
	imagen.show()
	gray = imagen.convert("L")
	gray.show()
	hola = gray.copy()
	width, height = imagen.size
	image_pixel2 = hola.load()
	image_pixel3 = gray.load()
	image_pixel = imagen.load()
	for h in range(height):
		for w in range(width):
			image_pixel2[w,h] = image_pixel[w,h][0]*0.2 + image_pixel[w,h][1]*0 + image_pixel[w,h][2]*0.8
			image_pixel3[w,h] = image_pixel2[w,h] - image_pixel3[w,h]
			
	imagen.show()			
	hola.show()	
	gray.show()				
	
	return gray

def get_image2():
#	os.system('uvccapture -d/dev/video1 -x1280 -y720')
#	os.system('uvccapture -m')
	imagen = Image.open('snap.jpg')
#	imagen = Image.open('blobs.jpg')

	gray = imagen.convert("L")
	gray.show("Gray")
	return gray


#######################################################
#Calcular threshold
#######################################################
def th(gray):
	min_value, max_value = gray.getextrema()
	th = 3*(max_value - min_value)/4.
	print "Th: ", th
	return th

##################################################################
#Crear nueva imagen en blanco y negro "puro" respecto al threshold
##################################################################
def blanco_negro(b_w):
	image_pixel = b_w.load()	
	width, height = b_w.size	
	th1 = th(b_w)
#	min_value, max_value = b_w.getextrema()
	for h in range(height):
		for w in range(width):
			pixel = image_pixel[w,h]
			if pixel < th1:
#			if pixel != max_value:
				image_pixel[w,h]= 255
			elif pixel >= th1:
#			else:
				image_pixel[w,h]= 0
	return b_w
	#guardamos la nueva imagen
	save_image(b_w, "b_w")
	#b_w.show()



###################################################################
#Idea... mundo perfecto... Muy lento
###################################################################
#def punto_laser(laser_image):
#	image_pixel = laser_image.load()
#	width, height = laser_image.size	
#	columnas = []
#	filas = []
#	#recorro la matriz
#	for h in range(4*height/9, 6*height/9):   
#		for w in range(width):
#			if image_pixel[w,h]== 0:
#				columnas.append(w)
#				filas.append(h)
#			
#	cmin= min(columnas)
#	cmax = max(columnas)
#	print "Cmin: ", cmin , "Cmax:" , cmax

#	fmin = min(filas)
#	fmax = max(filas)
#	print "Fmin: ", fmin,"Fmax:" ,fmax

#	punto = laser_image.crop((cmin,fmin,cmax,fmax))
#	save_image(punto, "punto")
##	print punto.size
##	punto.show()
#	return punto, cmin, fmin


def centroide(laser_image):
	image_pixel = laser_image.load()
	width, height = laser_image.size
	Cx = 0
	Cy = 0
	area = 0
#recorro la matriz
	for h in range(height):   
		for w in range(width):
			if image_pixel[w,h]== 0:
				Cx += w
				Cy +=h
				area += 1

	Centroide_x = (Cx/(area*1.0))
	Centroide_y = (Cy/(area*1.0))

	print "Size = " , width, height
	print "Centroide_x = " , Centroide_x ,  "Centroide_y = " , Centroide_y
	#laser_image.show()
	
	image_pixel[Centroide_x,Centroide_y] = 150
	#laser_image.show()
	save_image(laser_image, "punto2")
	return Centroide_x, Centroide_y

	

def Connected_com_label(b_w1):

	width, height = b_w1.size
	image_pixel = b_w1.load()
	for h in range(height):
		for w in range(width):
		#Blanco va a ser 0, negro 1
			if image_pixel[w,h] == 255:
				image_pixel[w,h] = 0
			else:
				image_pixel[w,h] = 1
						
	b_w1.show("0y1")
	
	v = []
	label = 2
	equivalencias = [0]*500
	image_pixel = b_w1.load()
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
	
	save_image(b_w1,"component_label")				
												
	return b_w1						
					
			
				
def main():
	#Obtener imagen en escala de grises
	gray = get_image2()
	print "Abrir"
	#gray = open_convert("blobs.jpg")
	

	width, height = gray.size
	b_w = gray.crop((0, 6*height/12, width, (6*height/12)+20))
#	b_w = gray.copy()
	
	
	b_w = blanco_negro(b_w)	
	b_w.show("b_w")
	
	b_w1 = b_w.copy()
	b_w1 = Connected_com_label(b_w1)
	b_w1.show("connected_com_label")

#	laser_image, cmin, fmin = punto_laser(b_w)
##	cmin = punto_laser(b_w)[1]
##	print cmin
##	fmin = punto_laser(b_w)[2]
##	print fmin
#	x_laser , y_laser = centroide(laser
#	
#	laser_image.show()
#	
#	coordenada = cmin + x_laser , fmin + y_laser
#	print coordenada
#	
#	x, y = centroide(b_w)
	
	
	#centroide(punto
	
#	hist =gray.histogram()
#	x = range(len(hist))
#	plt.figure(1)
#	plt.xlabel('Color')
#	plt.ylabel('Probability')
#	plt.title('Histogram of Color')
#	plt.plot(x,hist)

	

if __name__ == "__main__":
	main()

			

