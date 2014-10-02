#!/usr/bin/python

import Image


hola = Image.open("laser-ranger-1.jpg")
pimg = hola.convert("L")


#Aqui vamos a encontrar el max y min de la image, para hacer el threshold
width , height = pimg.size
print width  , height
image_pixels = pimg.load() 

#definimos las variables para guarda el max y el min
min_value=126
max_value= 126

#recorremos la imagen
for h in range(height):
	for w in range(width):
		#print width, height
		value = image_pixels[w, h]
		if value < min_value:#comparamos con el min
			min_value = value
		elif value>max_value:#comparamos con el max
			max_value = value
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
pimg2 = pimg.copy()
image_pixel = pimg2.load()	

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
pimg2.save("pil2.jpg")


###################################################################
#Crear nuevo objeto imagen
###################################################################
pimg3 = pimg2.copy()
image_pixel = pimg3.load()
datos = []

for h in range(height):
	for w in range(width):
		if image_pixel[w,h] == 0:
			datos.append([w,h])
#print datos




	








