#!/usr/bin/python

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
import matplotlib.pyplot as plt
import math

###################################################################
#Metodo para guardar un archivo y una imagen
###################################################################

#Metodo para guardar los datos
def write2file(hola, nombre):
	if type(hola) == list:
		f = open("Datos_pruebas/" + nombre +"." + datetime.datetime.now().ctime()+ ".txt", "w")
		f.writelines(["%s\n" % item  for item in hola])
		f.close()

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


#Obtener imagen en escala de grises
#gray = get_image2()
gray = open_convert("snap.jpg")

#Histograma y obtener valor umbral
histo = gray.histogram()
total_pixeles = gray.size[0]* gray.size[1]

#plotear el histograma
x = range(len(histo))
plt.plot(x,histo)
#plt.show()


probabilidades = []
for i in range(len(histo)):
	p = histo[i]/(total_pixeles*1.0)
	probabilidades.append(p)
#print probabilidades

#tiempo = (time.time() - time_start)
#print "Tiempo de cargar y convertir es" , tiempo
#print "Frames por segundo son " , 1/tiempo

#######################################################
#Obtener mayor intensidad y menor intensidad
#######################################################
def max_min(gray):
	max_min = gray.getextrema()
	min_value = max_min[0]
	max_value = max_min[1]
#	print min_value, max_value
	return min_value, max_value


#######################################################
#Calcular threshold
#######################################################
def th(gray):
	min_value, max_value = max_min(gray)
	th = 3*(max_value - min_value)/4.
	print "Th: ", th
	return th



##################################################################
#Crear nueva imagen en blanco y negro "puro" respecto al threshold
##################################################################
b_w = gray.copy()
image_pixel = b_w.load()	
width, height = b_w.size
#si el valor del pixel esta por encima del threshold entonces lo ponemos en negro, si es menor, entonces en blanco 
#por lo que el punto del laser se va a ver en la imagen como un punto negro	
th = th(b_w)
for h in range(height):
	for w in range(width):
		pixel = image_pixel[w,h]
		if pixel < th:
			image_pixel[w,h]= 255
		elif pixel >= th:
			image_pixel[w,h]= 0

#guardamos la nueva imagen
save_image(b_w, "b_w")
b_w.show()



###################################################################
#Idea... mundo perfecto... Muy lento
###################################################################
laser_image= b_w.copy()
image_pixel = laser_image.load()
columnas = []
filas = []
#recorro la matriz
for h in range(height):   
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
print punto.size
punto.show()


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

	Centroide_x = round(Cx/(area*1.0))
	Centroide_y = round(Cy/(area*1.0))

	print "Size = " , width, height
	print "Centroide_x = " , Centroide_x ,  "Centroide_y = " , Centroide_y
	
	return Centroide_x, Centroide_y
	

centroide(laser_image)
punto.show()
centroide(punto)




			

