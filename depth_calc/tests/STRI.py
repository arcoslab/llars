#!/usr/bin/python

from PIL import Image
from PIL import ImageFilter
import numpy as np
import cv2
import datetime
import os
import time


#HELP MODULES


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
#Capturar la imagen con OpenCV y convertirla a PIL
#######################################################

#capturamos la imagen de la camara web
def get_image():
	time_start = time.time()
	capture = cv2.cv.CaptureFromCAM(0) #webcam 
	img = cv2.cv.QueryFrame(capture)   #img is a OpenCV image
	cv2.cv.SaveImage("Imagenes_pruebas/image_color" +"." + datetime.datetime.now().ctime() +".jpg",img) #guardamos la imagen (prueba)
	#convertimos la imagen a escala de grises
	gray_cv = cv2.cv.CreateImage(cv2.cv.GetSize(img), 8,1) #8bits
	cv2.cv.CvtColor(img, gray_cv, cv2.cv.CV_RGB2GRAY)# (src,dst,code)
	gray = Image.fromstring("L", cv2.cv.GetSize(gray_cv), 			gray_cv.tostring()) #pimg is a PIL image
	tiempo = (time.time() - time_start)
	print "Tiempo de cargar y convertir es" , tiempo
	print "Frames por segundo son " , 1/tiempo
	return gray

def get_image2():
	os.system('uvccapture -m')
	imagen = Image.open('snap.jpg')
	gray = imagen.convert("L")
	return gray
	

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
#	print th
	return th



#CODE STRUCTURE

#######################################################
#Capturar la imagen y convertirla a escala de grises
#######################################################

#Obtener imagen en escala de grises

gray = get_image2()
save_image(gray, "gray")


#######################################################
#Punto de mayor luminosidad... 
#######################################################
max_luminosity = gray.copy()
image_pixel = max_luminosity.load()	
width, height = max_luminosity.size
max_value = max_min(gray)[1]
for h in range(height):
	for w in range(width):
		if image_pixel[w,h] == max_value:
			image_pixel[w,h]= 0
		else:
			image_pixel[w,h]= 255
	
save_image(max_luminosity, "max_luminosity")
max_luminosity.show()	    


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
contour = b_w.filter(ImageFilter.CONTOUR)
save_image(contour,"contorno")
contour.show()




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
		if image_pixel[w,h]==0:
			columnas.append(w)
			filas.append(h)

cmin= min(columnas)
cmax = max(columnas)
print cmin,cmax

fmin = min(filas)
fmax = max(filas)
print fmin,fmax

#write2file(columnas,"columnas")

punto = laser_image.crop((cmin,fmin,cmax,fmax))
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
#		if image_pixel[w,h]== 0:
#			w_in , h_in = w_fin , h_fin = w, h
#			

