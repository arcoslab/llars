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
		f.writelines(["%s\n" % item  for item in hola])
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
pfcs1 = []
pfcs2 = []
Centroides_x1 = []
Centroides_x2 = []
distancias_medidas1 = []
datos1 = []
m_bs1 = []

distancias_medidas2 = []
datos2 = []
m_bs2 = []

##realizar 50 mediciones... de los 18cm a los 6.2m (cada 5cm)
try:
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)
	
	while(i<50):
		
		GPIO.output(7, GPIO.HIGH)
		os.system('uvccapture -d/dev/video0 -x1280 -y720')
	#	os.system('uvccapture -m')
		GPIO.output(7, GPIO.LOW)
		
		imagen = Image.open('snap.jpg')
		print imagen.size
		gray = imagen.convert("L")
		gray.save("imagenes/gray_"+ str(i) +".jpg")
		width, height = gray.size
#		b_w = gray.copy()
		gray = gray.crop((0, 4*height/9, width, 5*height/9))
		gray.save("imagenes/gray_crop_"+ str(i) +".jpg")
		b_w = gray.copy()
	#	b_w.show()
		min_value, max_value = b_w.getextrema()
		print max_value, min_value
		th = 3*(max_value - min_value)/4.

	#Para calcular el centroide	
		Cx1 = 0
		Cy1 = 0
		area1 = 0

                b_w1 = b_w.copy()
		image_pixel = b_w1.load()	
		width1, height1 = b_w1.size	
		for h in range(height1):
			for w in range(width1):
				pixel = image_pixel[w,h]
				if  234<pixel<241 :
					image_pixel[w,h]= 255
					Cx1 += w
					Cy1 +=h
					area1 += 1					
				else :
					image_pixel[w,h]= 0

		b_w1.save("imagenes/b_w_th"+ str(i) +".jpg")

                Centroide_x1 = (Cx1/(area1*1.0))
		Centroide_y1 = (Cy1/(area1*1.0))
		print "Centroide_x1 = " , Centroide_x1 ,  "Centroide_y1 = " , Centroide_y1, "Area1 = " , area1


                Cx2 = 0
                Cy2 = 0
		area2 = 0

                b_w2 = b_w.copy()
		image_pixel = b_w2.load()	
		width1, height1 = b_w2.size	
		for h in range(height1):
			for w in range(width1):
				pixel = image_pixel[w,h]
				if pixel != max_value:
					image_pixel[w,h]= 0
				elif pixel == max_value:
					image_pixel[w,h]= 255
					Cx2 += w
					Cy2 +=h
					area2 += 1

		b_w2.save("imagenes/b_w_max"+ str(i) +".jpg")		    
	
		Centroide_x2 = (Cx2/(area2*1.0))
		Centroide_y2 = (Cy2/(area2*1.0))
		print "Centroide_x2 = " , Centroide_x2 ,  "Centroide_y2 = " , Centroide_y2, "Area2 = " , area2
	

##		Centroides_x.append(Centroide_x)
##
##		d_real = float(raw_input("Digite la distancia real en cm:  "))
##		distancias_medidas.append(d_real)
##	
##		pfc = Centroide_x - ((width-1)/2.0)
##		
##		pfcs.append(pfc)
##		
##		# (x,y)
##		datos.append((d_real, pfc))
##	
		i +=1
		raw_input("Press Enter to continue...")
##
##	while j < len(datos)-1:
##		#m_b = (m,b)
##		m_b = recta(datos[j],datos[j+1])
##		m_bs.append(m_b)
##		j+=1
##	
##	print m_bs
	
	GPIO.cleanup()
##	write2file(m_bs,"m_bs")
##	write2file(datos, "datos")
##	write2file(pfcs, "pfcs" )
##	write2file(distancias_medidas, "distancias")

	sys.exit(1)
	
except KeyboardInterrupt:
	GPIO.cleanup()
##	write2file(datos, "datos")
##	write2file(pfcs, "pfcs" )
##	write2file(distancias_medidas, "distancias")
	sys.exit(1)

	
