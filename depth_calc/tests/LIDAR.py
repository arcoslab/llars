#!/usr/bin/python

from PIL import Image
import os
import matplotlib.pyplot as plt
import sys
from PyQt4 import QtGui,QtCore
import datetime

#try: 
#	import RPi.GPIO as GPIO

#except:
#	print "Try running as sudo... for GPIO library"	


def write2file(hola, nombre):
	if type(hola) == list:
		f = open( nombre +".txt", "w")
		for i in hola:
			f.write(str(i))
			f.write(',')
		f.close()


#Insertar los datos de la calibracion, serian los datos (m,b) de cada parte y los pfcs usados en la calibracion.. para hacer acceso 
pfcs = [-77, -58, -51, -37 , -28, -19, -13, -5, 2, 4, 5, 9.5, 14, 16, 20, 20.5, 21, 23.5, 24, 26.6666666667, 27.5, 30, 31, 32, 33, 34, 35, 41]

m_bs = [(0.2631578947368421, 50.26315789473684), (0.7142857142857143, 76.42857142857143), (0.35714285714285715, 58.214285714285715), 
(0.5555555555555556, 65.55555555555556), (0.5555555555555556, 65.55555555555556), (0.8333333333333334, 70.83333333333333), (0.625, 68.125), (0.7142857142857143, 68.57142857142857), (2.5, 65.0), (5.0, 55.0), (1.1111111111111112, 74.44444444444444), (1.1111111111111112, 74.44444444444444), (2.5, 55.0), (1.4285714285714286, 72.14285714285714), (10.0, -95.0), (5.0, 5.0), (2.0, 68.0), (10.0, -120.0), (1.874999999976563, 75.0000000005625), (6.000000000239996, -35.00000000659989), (4.0, 20.0), (5.0, -10.0), (5.0, -10.0), (5.0, -10.0), (5.0, -10.0), (5.0, -10.0), (7.5, -97.5)]




#Inicializar variables		
i = 1
mediciones = []
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7, GPIO.OUT)

try:

	while(1):
	#	GPIO.output(7, GPIO.HIGH)
	#	os.system('uvccapture -d/dev/video0 -x1280 -y720')
	#	os.system('uvccapture -m')
	#	GPIO.output(7, GPIO.LOW)
	
		imagen = Image.open('snap.jpg')
		gray = imagen.convert("L")
		gray.save("imagenes/gray_"+ datetime.datetime.now().ctime() +".jpg")
		width, height = gray.size
	#	b_w = gray.copy()
		b_w = gray.crop((0, 3*height/8, width, (7*height/8)))
		b_w.show()
		min_value, max_value = b_w.getextrema()
		th = 3*(max_value - min_value)/4.

		#Para calcular el centroide	
		Cx = 0
		Cy = 0
		area = 0

		image_pixel = b_w.load()	
		width1, height1 = b_w.size	
		for h in range(height1):
			for w in range(width1):
				pixel = image_pixel[w,h]
				if pixel != max_value:
					image_pixel[w,h]= 0 #blanco , background
				elif pixel == max_value:
					image_pixel[w,h]= 1 #negro

						
	
		v = []
		label = 2
		equivalencias = [0]*500
		image_pixel = b_w.load()
		for h in range(height):
			for w in range(width):
				if (w == 0 or h == 0 or w == (width-1)):
					image_pixel[w,h] = 0  #esquinas... background
					pass
					
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
	
		for h in range(height):
			for w in range(width):
				#if equivalencias[image_pixel[w,h]] != 0:		
				image_pixel[w,h] = equivalencias[image_pixel[w,h]]

		histo = b_w.histogram()
		minimo, maximo = b_w.getextrema()
		
		write2file(histo, "histo")
		print minimo, maximo


#					Cx += w
#					Cy +=h
#					area += 1
#					
#		
#							

#		b_w.save("imagenes/b_w_"+ str(i) +".jpg")
#	
#		Centroide_x = (Cx/(area*1.0))
#		Centroide_y = (Cy/(area*1.0))
#		pfc = Centroide_x - ((width-1)/2.0)
#		
#		i = 0		
#		while(i < len(pfcs)):
#			if pfc > pfcs[i]:
#				i +=1
#				#print "i",i
#				if i >= len(pfcs):
#					print "fuera del alcance de medicion"	
#			
#			else:
#				print"pfc", pfc, "i = ", i, "m =" , m_bs[i-1][0], "b =" , m_bs[i-1][1]
#				distancia = m_bs[i-1][0]* pfc + m_bs[i-1][1]
#				i = len(pfcs)
#				print "distancia",distancia

#		
#		medidas.append((distancia, pfc))

#		print "Centroide_x = " , Centroide_x ,  "Centroide_y = " , Centroide_y, "Area = " , area, "Distancia = ", distancia, "pfc = " , pfc	
#		raw_input("Press Enter to continue...")


	#GPIO.cleanup()
	sys.exit(1)
	
except KeyboardInterrupt:
	#GPIO.cleanup()
	write2file(pfcs, "pfcs" )
	sys.exit(1)

	
