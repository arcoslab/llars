#!/usr/bin/python

from PIL import Image
import sys, os
from PyQt4 import QtGui,QtCore


#app = QtGui.QApplication(sys.argv)
#window=QtGui.QWidget()
#tableWidget = QtGui.QTableWidget()
#tableWidget.setRowCount(2)
#tableWidget.setColumnCount(3)

##dato_distancia=QtGui.QLineEdit()
#salirButton = QtGui.QPushButton("Exit",window)
#continuarButton = QtGui.QPushButton("Continue",window)
##plotearButton = QtGui.QPushButton("Plot",window)
#pic = QtGui.QLabel()
#pic.setGeometry(10, 10, 400, 100)
#layout = QtGui.QVBoxLayout()
##layout.addWidget(dato_distancia)
#layout.addWidget(tableWidget)
#layout.addWidget(salirButton)
#layout.addWidget(continuarButton)
#window.setLayout(layout)
#window.setWindowTitle("Laser Range Finder")
#window.show()

##os.system('uvccapture -m')
#tableWidget.setItem(1, 1, pic)

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

pic3 = QtGui.QLabel()

imagen = QtGui.QVBoxLayout()
imagen.addWidget(dato_max)
imagen.addWidget(dato_max1)
imagen.addWidget(dato_th)
imagen.addWidget(dato_th1)
imagen.addWidget(pic3)

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

imagen = Image.open('laser-ranger-12.jpg')
gray = imagen.convert("L")
gray.save("imagenes/gray.jpg")
pic.setPixmap(QtGui.QPixmap("imagenes/gray.jpg"))
pic2.setPixmap(QtGui.QPixmap("imagenes/gray.jpg"))
pic3.setPixmap(QtGui.QPixmap("imagenes/gray.jpg"))

def salir():
#	global pfcs, distancias_medidas
#	write2file(pfcs, "pfcs" )
#	write2file(distancias_medidas, "distancias")
##	plt.plot(pfcs,distancias_medidas)
##	plt.show()
#	plotear()
	sys.exit(0)

#def plotear():
#	global pfcs
#	global distancias_medidas
#	plt.figure(1)          
#	plt.xlabel('Points from center')
#	plt.ylabel('Distancias')
#	plt.title('Distancia vs pfc')
#	plt.plot(pfcs,distancias_medidas)
#	#savefig('distancia_pfc.png')
#	plt.show()




##Conexion del clic en el botton
#QtCore.QObject.connect(salirButton,QtCore.SIGNAL("clicked()"),salir)
#QtCore.QObject.connect(continuarButton,QtCore.SIGNAL("clicked()"),i_mas1)
#QtCore.QObject.connect(plotearButton,QtCore.SIGNAL("clicked()"),plotear)
##QtCore.QObject.connect(datoButton,QtCore.SIGNAL("clicked()"),dato)

sys.exit(app.exec_())


