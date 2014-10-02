#!/usr/bin/python

import math
import cv2

color = [0,255,0] #color verde del laser
coordenada_central = [640, 384] # punto central de una imagen de resolucion 1280x768
#ocupo saber en un cm cuantos pixeles hay para poder calcular la distancia del centro a donde esta el laser
#rango de vision de la camara

def relacion_pixel_cm(distancia_real, diferencia_coordenadas)
	relacion_pixel_cm = distancia_real/diferencia_coordenadas
	return relacion_pixel_cm

pixeles_camara_h = 1280
l = relacion_pixel_cm * pixeles_camara_h


coef_divergencia_laser = 1 * (10**(-3)) #1mrad

delta_D = 2 * l * math.tan( 2 * coef_divergencia_laser) 




relacion_pixel_cm = 0.1  #10 pixeles en un cm (random, hay q verlo se hace con la calibracion)
angulo_laser = math.pi/3 #angulo fijo del laser respecto a la horizontal de la camara 60 grados
l = 5 #5 cm distancia entre laser y camara

# "entrada" hay q obtenerl con modulo de calculo de coordenada
h = l * math.tan(angulo_laser) #ditancia de la camara al punto donde se cruza con el laser
 

def Range(self, entrada):
	d_2 = (coordenada_central.[0] - entrada.[0]) * relacion_pixel_cm #para convertirlo en cm

	if d_2 == 0: # en el puro centro
		h_1 = h

	if d_2 > 0: # a la derecha
		h_2 = d_2 * math.pi(angulo_laser)
		h_1 = h - h_2

	if d_2 < 0: # a la izquierda
		d_2 = -d_2
		h_2 = d_2 * math.pi(angulo_laser)
		h_1 = h + h_2

return(h_1)	



		








