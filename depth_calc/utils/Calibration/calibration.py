#!/usr/bin/python

from PIL import Image
import os
import matplotlib.pyplot as plt
import sys
from PyQt4 import QtGui,QtCore


def write2file(hola, nombre):
	if type(hola) == list:
		f = open( nombre +".txt", "w")
		f.writelines(["%s\n" % item  for item in hola])
		f.close()


#ventana
app=QtGui.QApplication(sys.argv)
datos=QtGui.QWidget()
pictures=QtGui.QWidget()

dato_distancia=QtGui.QLabel()
dato_distancia.setText("Distancia medida")

dato_distancia1=QtGui.QLabel()
dato_distancia1.setText("0")

dato_th=QtGui.QLabel()
dato_th.setText("Threshold")

dato_th1=QtGui.QLabel()
dato_th1.setText("0")

dato_max=QtGui.QLabel()
dato_max.setText("Valor maximo")

dato_max1=QtGui.QLabel()
dato_max1.setText("0")

dato_pfc=QtGui.QLabel()
dato_pfc.setText("pfc")

dato_pfc1=QtGui.QLabel()
dato_pfc1.setText("0")

pic = QtGui.QLabel()

pic2 = QtGui.QLabel()

#pic3 = QtGui.QLabel()

imagen = QtGui.QVBoxLayout()
imagen.addWidget(dato_max)
imagen.addWidget(dato_max1)
imagen.addWidget(dato_th)
imagen.addWidget(dato_th1)
#imagen.addWidget(pic3)

layout = QtGui.QVBoxLayout()
layout.addWidget(dato_distancia)
layout.addWidget(dato_distancia1)
layout.addWidget(pic)
layout.addWidget(pic2)
layout.addWidget(dato_pfc)
layout.addWidget(dato_pfc1)

datos.setLayout(layout)
datos.setWindowTitle("Laser Range Finder Data")
datos.show()


pictures.setLayout(imagen)
pictures.setWindowTitle("Laser Range Finder Histogram")
pictures.show()


#Inicializar vectores
Centroides_x = []
distancias_medidas = []
pfcs = []	

i = 1

##realizar 120 mediciones... de los 18cm a los 6.2m (cada 5cm)
while(i<5):
#	os.system('uvccapture -d/dev/video1-x1280 -y720')
#	os.system('uvccapture -m')
#	imagen = Image.open('snap.jpg')
	gray = Image.open('imagenes/gray_1.jpg')
#	gray = imagen.convert("L")
#	gray.save("imagenes/gray_"+ str(i) +".jpg")
	pic.setPixmap(QtGui.QPixmap("imagenes/gray_"+ str(i) +".jpg"))
	width, height = gray.size
	b_w = gray.copy()
#	b_w = gray.crop((0, 3*height/8, width, (7*height/8)))
#	b_w.show()
	min_value, max_value = b_w.getextrema()
	dato_max1.setText(str(max_value))
	th = 3*(max_value - min_value)/4.
	dato_th1.setText(str(th))
	
#	y =gray.histogram()
#	x = range(len(y))
#	plt.xlabel('Color')
#	plt.ylabel('Probability')
#	plt.title('Histogram of Color')
#	plt.plot(x,y)
#	plt.savefig("imagenes/Histograma_"+ str(i) +".jpg")
#	pic3.setPixmap(QtGui.QPixmap("imagenes/Histograma_"+ str(i) +".jpg"))
	
	
	Cx = 0
	Cy = 0
	area = 0
	
	image_pixel = b_w.load()	
	width1, height1 = b_w.size	
	for h in range(height1):
		for w in range(width1):
			pixel = image_pixel[w,h]
			if pixel != max_value:
				image_pixel[w,h]= 255
			elif pixel == max_value:
				image_pixel[w,h]= 0
				Cx += w
				Cy +=h
				area += 1

	b_w.save("imagenes/b_w_"+ str(i) +".jpg")
	pic2.setPixmap(QtGui.QPixmap("imagenes/b_w_"+ str(i) +".jpg"))
	
	Centroide_x = (Cx/(area*1.0))
	Centroide_y = (Cy/(area*1.0))
	print "Centroide_x = " , Centroide_x ,  "Centroide_y = " , Centroide_y
	

	Centroides_x.append(Centroide_x)

	d_real = float(raw_input("Digite la distancia real en cm:  "))
	dato_distancia1.setText(str(d_real))
	distancias_medidas.append(d_real)
	
	
	pfc = Centroide_x - ((width-1)/2.0)
	pfcs.append(pfc)
	dato_pfc1.setText(str(pfc))

	
	
	i +=1
	raw_input("Press Enter to continue...")
	

	
write2file(pfcs, "pfcs" )
write2file(distancias_medidas, "distancias")

print pfcs 
print distancias_medidas


#plt.figure(1)
##plt.subplot(211)          
#plt.xlabel('Points from center')
#plt.ylabel('Distancias')
#plt.title('Distancia vs pfc')
#plt.plot(pfcs,distancias_medidas)
##plt.subplot(211)          



#plt.figure.savefig('distancia_pfc.png')
#plt.show()

#savefig('distancia_vs_pfc.jpg')

sys.exit(app.exec_())	




	
	
