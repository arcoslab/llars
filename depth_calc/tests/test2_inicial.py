#!/usr/bin/python

import Image, ImageFilter
import numpy as np
import cv2


#######################################################
#Capturar la imagen 
#######################################################


#abrir imagen  y convertirla a escala de grises (1 canal)
imagen = Image.open("laser-ranger-2.jpg")
gray = imagen.convert("L")


#######################################################
#Obtener mayor intensidad y menor intensidad
#######################################################

#funcion para obtener valor maximo y minimo
max_min = gray.getextrema()

min_value = max_min[0]
max_value = max_min[1]

#imprimir los valores
print min_value, max_value


#######################################################
#Calcular threshold
#######################################################

#calculo valor del threshold
th = 3*(max_value - min_value)/4
print th


##################################################################
#Crear nueva imagen en blanco y negro "puro" respecto al threshold
##################################################################

#copiamos la imagen a una nueva
b_w = gray.copy()
image_pixel = b_w.load()	
width, height = b_w.size

#si el valor del pixel esta por encima del threshold entonces lo ponemos en negro, si es menor, entonces en blanco 
#por lo que el punto del laser se va a ver en la imagen como un punto negro	
for h in range(height):
	for w in range(width):
		pixel = image_pixel[w,h]
		if pixel < th:
			image_pixel[w,h]= 255
		elif pixel >= th:
			image_pixel[w,h]= 0
#guardamos la nueva imagen
b_w.save("b_w.jpg")
b_w.show()


###################################################################
#Encontrar contorno
###################################################################
#obtener el contorno de la imagen
contour = b_w.filter(ImageFilter.CONTOUR)
contour.save("contorno.jpg")
#contour.show()


#para guardar lista en un documento
def write2file(hola):
	if type(hola) == list:
		f = open("datos", "w")
		for i in hola:
			f.write(str(i))
	f.close()


###################################################################
#Crear nuevo objeto imagen
###################################################################
laser_image= b_w.copy()
image_pixel = laser_image.load()

columnas = []
filas = []
i = 0
#j = 0

#recorro la matriz
for h in range(height):   
	for w in range(width):
		if image_pixel[w,h]==0:
			columnas.append(w)
			filas.append(h)

#			i = i+1

cmin= min(columnas)
cmax = max(columnas)
print cmin,cmax

fmin = min(filas)
fmax = max(filas)
print fmin,fmax

punto = laser_image.crop((cmin,fmin,cmax,fmax))
punto.show()
punto.save("laser.jpg")

		
###################################################################
#Crear nuevo objeto imagen
###################################################################
laser_image= b_w.copy()
image_pixel = laser_image.load()
win=[]
matriz = []
ii = []
for h in range(height):
	w = 0
	i = 0
	j =0
	while image_pixel[w,h]==255:	
		w += 1

		if w == (width - 1):
			break

	else: 
		if i == 0:
			win.append[w]

		i += 1
		w += 1

		if image_pixel[w+1,h] == 255:
			j +=1
			win.append[i]
			matriz[j].append(win)
			
		if w == (width - 1):
			break


		


#cuando encuentro un pixel negro en la fila genero un contador para contar cuantos negros hay en la fila
#y asi obtener la columna central
#		while image_pixel[w,h] == 0:
#			columnas.append(w)
#			i = i + 1
#			print i
		
#		cc = 2*columnas[0] + i / 2
#		print cc

#cuando encuentro un pixel negro en la columna genero un contador para contar cuantos negros hay en la columna
#y asi obtener la fila central
#for w in range(width):
#	for h in range(height):
#		while image_pixel[w,h] == 0:
#			filas.append(h)
#			j = j + 1
#			print j
				
#				jc = 2*filas[0]+j/2
#				print jc



#coordenada = jc, cc


#laser_image.crop((208,63,218,72)).show()



#print datos




