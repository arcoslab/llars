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
	os.system('uvccapture -d/dev/video1')
	imagen = Image.open('snap.jpg')
	gray = imagen.convert("L")
	gray.show()
	return gray


#Obtener imagen en escala de grises

#time_start = time.time()
#gray = open_convert("laser-ranger-2.jpg")
gray = get_image2()

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

#######################################################
#Punto de mayor luminosidad... 
#######################################################
#max_luminosity = gray.copy()
#image_pixel = max_luminosity.load()	
#width, height = max_luminosity.size
#max_value = max_min(gray)[1]
#for h in range(height):
#	for w in range(width):
#		if image_pixel[w,h] == max_value:
#			image_pixel[w,h]= 0
#		else:
#			image_pixel[w,h]= 255
#	
#save_image(max_luminosity, "max_luminosity")
#max_luminosity.show()	    




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
#Encontrar contorno
###################################################################
#obtener el contorno de la imagen
#contour = b_w.filter(ImageFilter.CONTOUR)
#save_image(contour,"contorno")
#contour.show()




###################################################################
#Idea... mundo perfecto... Muy lento
###################################################################
laser_image= b_w.copy()
image_pixel = laser_image.load()
datos = []
columnas = []
filas = []
mancha = []



#recorro la matriz
for h in range(height):   
	for w in range(width):
		if image_pixel[w,h]==0:
			datos.append([w,h])
			columnas.append(w)
			filas.append(h)


cmin= min(columnas)
cmax = max(columnas)
print "Cmin: ", cmin , "Cmax:" , cmax

fmin = min(filas)
fmax = max(filas)
print "Fmin: ", fmin,"Fmax:" ,fmax


write2file(datos, "datos")


#write2file(columnas,"columnas")
coordenadas = [cmin,fmin,cmax,fmax]
write2file(coordenadas,"coordenadas")

#Declaro el punto
punto = laser_image.crop((cmin,fmin,cmax,fmax))



#Centroide
coordenada_x =0
for i in range(len(columnas)):
	coordenada_x +=columnas[i]	

coordenada_x = math.floor(coordenada_x/(len(columnas)*1.0))
print "coordenada_x", coordenada_x


coordenada_y =0
for i in range(len(filas)):
	coordenada_y +=filas[i]	

coordenada_y = math.floor(coordenada_y/(len(filas)*1.0))
print "coordenada_y", coordenada_y



#Muestro el punto
image_pixel[coordenada_x,coordenada_y]= 100
punto.show()
save_image(punto, "laser")



###################################################################
#Idea de Eduardo
###################################################################

#laser_image= b_w.copy()
#image_pixel = laser_image.load()
#win=[]
#matriz = []
#ii = []
#for h in range(height):
#	w = 0
#	i = 0
#	j =0
#	while image_pixel[w,h]==255:	
#		w += 1

#		if w == (width - 1):
#			break

#	else: 
#		if i == 0:
#			win.append[w]

#		i += 1
#		w += 1

#		if image_pixel[w+1,h] == 255:
#			j +=1
#			win.append[i]
#			matriz[j].append(win)
#			
#		if w == (width - 1):
#			break


###########################################################
#Idea de Fernando
###########################################################
#for h in range(height):
#	for w in range(width):
#		if image_pixel[w,h]== 255:
#			continue

#		elif image_pixel[w,h]== 0:
#			i +=1
#			if i == 1:
#				w_in , h_in = w, h
#	
#			else:
			

			
			
				








			

