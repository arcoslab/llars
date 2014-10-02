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
		f = open("Datos_pruebas/"+ nombre +".txt", "w")
		for i in hola:
			f.write(str(i))
			f.write('\n')
		f.close()


#Insertar los datos de la calibracion, serian los datos (m,b) de cada parte y los pfcs usados en la calibracion.. para hacer acceso 
#pfcs = [-77, -58, -51, -37 , -28, -19, -13, -5, 2, 4, 5, 9.5, 14, 16, 20, 20.5, 21, 23.5, 24, 26.6666666667, 27.5, 30, 31, 32, 33, 34, 35, 41]

#m_bs = [(0.2631578947368421, 50.26315789473684), (0.7142857142857143, 76.42857142857143), (0.35714285714285715, 58.214285714285715), 
#(0.5555555555555556, 65.55555555555556), (0.5555555555555556, 65.55555555555556), (0.8333333333333334, 70.83333333333333), (0.625, 68.125), (0.7142857142857143, 68.57142857142857), (2.5, 65.0), (5.0, 55.0), (1.1111111111111112, 74.44444444444444), (1.1111111111111112, 74.44444444444444), (2.5, 55.0), (1.4285714285714286, 72.14285714285714), (10.0, -95.0), (5.0, 5.0), (2.0, 68.0), (10.0, -120.0), (1.874999999976563, 75.0000000005625), (6.000000000239996, -35.00000000659989), (4.0, 20.0), (5.0, -10.0), (5.0, -10.0), (5.0, -10.0), (5.0, -10.0), (5.0, -10.0), (7.5, -97.5)]




#Inicializar variables		
i = 1
mediciones = []
pfcs = []	
Centroides_x = []

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7, GPIO.OUT)

try:

	while(i<60):
	#	GPIO.output(7, GPIO.HIGH)
	#	os.system('uvccapture -d/dev/video0 -x1280 -y720')
		os.system('uvccapture -m')
	#	GPIO.output(7, GPIO.LOW)
	
		imagen = Image.open('snap.jpg')
		gray = imagen.convert("L")
		gray.save("imagenes/gray_"+ str(i) +".jpg")
		width, height = gray.size
#		b_w = gray.copy()
		b_w = gray.crop((0, 6*height/12 - 20, width, (6*height/12) + 20))
#		b_w.show()
		min_value, max_value = b_w.getextrema()
#		th = 3*(max_value - min_value)/4.
		th = 0.88*(max_value - min_value)

		#Para calcular el centroide	

		image_pixel = b_w.load()	
		width1, height1 = b_w.size	
		for h in range(height1):
			for w in range(width1):
				pixel = image_pixel[w,h]
				if pixel < th:
					image_pixel[w,h]= 0 #blanco , background
				elif pixel >= th:
					image_pixel[w,h]= 1 #negro

#		b_w.show()					
	
		v = []
		label = 2
		#como mejorar el numero de etiquetas y el valor de equivalencias???
		equivalencias = [0]*300
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
						
						#si todos mis vecinos son cero y yo soy uno, entonces new label					
						if not vecinos:
							image_pixel[w,h] = label
							label += 1
					
						#sino coloco valor de minimo de los vecinos  
						else:				  
							min_vecino = min(vecinos)
#							max_vecino = max(vecinos)
							image_pixel[w,h] = min_vecino
							
							#podria revisar si los vecinos son iguales o si solo tengo uno vecino, para no entrar al vector a hacer tonto
							for x in range(len(vecinos)):
								if (equivalencias[vecinos[x]] == 0 or equivalencias[vecinos[x]] > min_vecino):
									equivalencias[vecinos[x]] = min_vecino
						
		write2file(v,"vecinos")

		write2file(equivalencias,"equivalencias")
		
	
	#imagen con min_vecinos o min_labels
		for h in range(height1):
			for w in range(width1):
				#print image_pixel[w,h]
				#if equivalencias[image_pixel[w,h]] != 0:		
				image_pixel[w,h] = equivalencias[image_pixel[w,h]]
		
#		b_w.show()
		
		histo = b_w.histogram()
		minimo, maximo = b_w.getextrema()
		
		write2file(histo, "histo")
		print minimo, maximo

#		i = 2?	 wtf
		i +=1

		print label
		
		blobs = []
		image_pixel = b_w.load()
		for j in range(1,len(histo)):
			if histo[j]>20 and histo[j]<500:
#			if histo[j]>100 and histo[j]<5000:		
				print "label", j
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
				
				#discriminando segun Centroide_y
				if (height1/2 - 5 < Centroide_y < height1/2 +5):				
					pfc = round(Centroide_x - ((width-1)/2.0))
					blobs.append((j, Centroide_x, Centroide_y))
					image_pixel[Centroide_x, Centroide_y] = 255
							
#		b_w.show()
		print blobs							
		
							
		b_w.save("imagenes/b_w_"+ str(i) +".jpg")
	
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


#	GPIO.cleanup()
	sys.exit(1)
	
except KeyboardInterrupt:
	#GPIO.cleanup()
	write2file(pfcs, "pfcs" )
	sys.exit(1)

	
