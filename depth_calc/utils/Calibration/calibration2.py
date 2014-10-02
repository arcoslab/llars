#!/usr/bin/python

from PIL import Image
import os
import matplotlib.pyplot as plt
import sys
from PyQt4 import QtGui,QtCore

try: 
	import RPi.GPIO as GPIO

except:
	print "Try running as sudo... for GPIO library"	


def write2file(hola, nombre):
	if type(hola) == list:
		f = open( nombre +".txt", "w")
		f.writelines(["%s," % item  for item in hola])
		f.close()

def recta(par1, par2):
#par = (pfc, distancia)	
#distancia = m pfc + b		
	m = (par2[1]- par1[1])/((par2[0] - par1[0])*1.0)
	b = par1[1] - m * par1[0]
	m_b = m,b
	#return (m,b)
	return m_b
	

#Inicializar variables		
i = 1
pfcs = []	
Centroides_x = []
distancias_medidas = []
datos = []
m_bs = []

##realizar 120 mediciones... de los 18cm a los 6.2m (cada 5cm)
try:
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)
	
	while(i<30):
		
		GPIO.output(7, GPIO.HIGH)
	#	os.system('uvccapture -d/dev/video0 -x1280 -y720')
		os.system('uvccapture -m')
		GPIO.output(7, GPIO.LOW)
		
		imagen = Image.open('snap.jpg')
		gray = imagen.convert("L")
		gray.save("imagenes/gray_"+ str(i) +".jpg")
		width, height = gray.size
	#	b_w = gray.copy()
		b_w = gray.crop((0, 6*height/12, width, (6*height/12)+20))
	#	b_w.show()
		min_value, max_value = b_w.getextrema()
		th = 3*(max_value - min_value)/4.


		#Para calcular el centroide	
		image_pixel = b_w.load()	
		width1, height1 = b_w.size	
		for h in range(height1):
			for w in range(width1):
				pixel = image_pixel[w,h]
				if pixel < th:
					image_pixel[w,h]= 0 #"blanco" , background
				elif pixel >= th:
					image_pixel[w,h]= 1 #negro
	
		v = []
		label = 2
		equivalencias = [0]*255
		image_pixel = b_w.load()
		for h in range(height1):
			for w in range(width1):
				if (w == 0 or h == 0 or w == (width1-1)):
					image_pixel[w,h] = 0  #esquinas... background
					
				else:
					#si no es blanco, background
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
	
		for h in range(height1):
			for w in range(width1):
				print image_pixel[w,h]
				#if equivalencias[image_pixel[w,h]] != 0:		
				image_pixel[w,h] = equivalencias[image_pixel[w,h]]
		
#		b_w.show()
		
		histo = b_w.histogram()
		minimo, maximo = b_w.getextrema()
		
		write2file(histo, "histo")
		print minimo, maximo

		i = 2

		print label
		
		blobs = []
		image_pixel = b_w.load()
		for j in range(len(histo)):
			if histo[j]>80 and histo[j]<200:	
				Cx = 0
				Cy = 0
				area = 0
				for h in range(height1):
					for w in range(width1):
						if image_pixel[w,h] == j:
							Cx += w
							Cy +=h
							area += 1
						
				print "area" , area, "histo" , histo[j]
				Centroide_x = round(Cx/(area*1.0))
				Centroide_y = round(Cy/(area*1.0))
				pfc = round(Centroide_x - ((width-1)/2.0))
				blobs.append((j, Centroide_x, Centroide_y))
				image_pixel[Centroide_x, Centroide_y] = 255
							
		#b_w.show()
		print blobs							

##############################################################################
#Falta discernir entre varios blobs en caso de haberlos jeje
##############################################################################

		d_real = float(raw_input("Digite la distancia real en cm:  "))
		distancias_medidas.append(d_real)
	
		pfc = Centroide_x - ((width-1)/2.0)
		
		pfcs.append(pfc)
		
		# (x,y)
		datos.append((d_real, pfc))
	
		i +=1
		raw_input("Press Enter to continue...")

	while j < len(datos)-1:
		#m_b = (m,b)
		m_b = recta(datos[j],datos[j+1])
		m_bs.append(m_b)
		j+=1
	
	print m_bs
	
	GPIO.cleanup()
	write2file(m_bs,"m_bs")
	write2file(datos, "datos")
	write2file(pfcs, "pfcs" )
	write2file(distancias_medidas, "distancias")

	sys.exit(1)
	
except KeyboardInterrupt:
	GPIO.cleanup()
	write2file(datos, "datos")
	write2file(pfcs, "pfcs" )
	write2file(distancias_medidas, "distancias")
	sys.exit(1)

	
