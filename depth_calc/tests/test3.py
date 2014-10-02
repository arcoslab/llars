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
#import cv2
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
	gray = imagen.convert("L")
	return gray

def get_image2():
#	os.system('uvccapture -d/dev/video1 -x1280 -y720')
#	os.system('uvccapture -m')
	imagen = Image.open('snap.jpg')
	gray = imagen.convert("L")
	gray.show()
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
	for h in range(height):
		for w in range(width):
			pixel = image_pixel[w,h]
			if pixel < th1:
				image_pixel[w,h]= 255
			elif pixel >= th1:
				image_pixel[w,h]= 0
	return b_w
	#guardamos la nueva imagen
	save_image(b_w, "b_w")
	#b_w.show()



###################################################################
#Idea... mundo perfecto... Muy lento
###################################################################
def punto_laser(laser_image):
	image_pixel = laser_image.load()
	width, height = laser_image.size	
	columnas = []
	filas = []
	#recorro la matriz
	for h in range(4*height/9, 6*height/9):   
		for w in range(width):
			if image_pixel[w,h]== 0:
				columnas.append(w)
				filas.append(h)
			
	cmin= min(columnas)
	cmax = max(columnas)
	print "Cmin: ", cmin , "Cmax:" , cmax

	fmin = min(filas)
	fmax = max(filas)
	print "Fmin: ", fmin,"Fmax:" ,fmax

	punto = laser_image.crop((cmin,fmin,cmax,fmax))
	save_image(punto, "punto")
#	print punto.size
#	punto.show()
	return punto, cmin, fmin


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

	#print "Size = " , width, height
	#print "Centroide_x = " , Centroide_x ,  "Centroide_y = " , Centroide_y
	#laser_image.show()
	
	image_pixel[Centroide_x,Centroide_y] = 150
	#laser_image.show()
	save_image(laser_image, "punto2")
	return Centroide_x, Centroide_y



#def Range(self, entrada):
#	d_2 = (coordenada_central.[0] - entrada.[0]) * relacion_pixel_cm #para convertirlo en cm

#	if d_2 == 0: # en el puro centro
#		h_1 = h

#	if d_2 > 0: # a la derecha
#		h_2 = d_2 * math.pi(angulo_laser)
#		h_1 = h - h_2

#	if d_2 < 0: # a la izquierda
#		d_2 = -d_2
#		h_2 = d_2 * math.pi(angulo_laser)
#		h_1 = h + h_2

#return(h_1)	

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
	
	v = []
	label = 2
	equivalencias = []
	max_equivalencias = []
	min_equivalencias = []
	valores = []
	image_pixel = b_w1.load()
	for h in range(height):
		for w in range(width):

			if (w == 0 or h == 0 or w == (width-1)):
				pass
						
			else:
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
		
					#print vecinos
					
					v.append(vecinos)
					
					if not vecinos:
						image_pixel[w,h] = label
						#print label
						label += 1
					
					  
					else:				  
						min_equivalencia = min(vecinos)
						max_equivalencia = max(vecinos)
						max_equivalencias.append(max_equivalencia)
						image_pixel[w,h] = min_equivalencia
						if max_equivalencia !=	min_equivalencia:
							equivalencias.append((min_equivalencia,max_equivalencia))

	imagen = []
	image_pixel = b_w1.load()
	for h in range(height):
		for w in range(width):
			imagen.append(image_pixel[w,h])
	
		

	
	#print label
	#print max(equivalencias)							
	#print max(max_equivalencias)
						
						
#	for range
						
	write2file(imagen,'imagen')					
	write2file(v,'v')
	write2file(equivalencias,"equivalencias")	
	save_image(b_w1, "b_w1")
	
	
#	
#	image_pixel = b_w1.load()
#	hola = []
#	for h in range(height):
#		for w in range(width): 
#			hola.append(image_pixel[w,h])
#			
#	
#	f = open("Datos_pruebas/b_w1." + datetime.datetime.now().ctime()+ ".txt", "w")
#	
#	f.write(row for row in hola)
#	
#	#f.writelines(["%s" % item  for item in hola])
#	f.close
	return b_w1						
					
			
				
def main():
	#Obtener imagen en escala de grises
	#gray = get_image2()
	gray = open_convert("blobs.jpg")


	b_w = gray.copy()
	b_w = blanco_negro(b_w)	
	
	b_w1 = b_w.copy()
	b_w1 = Connected_com_label(b_w1)
	b_w1.show()

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

			

