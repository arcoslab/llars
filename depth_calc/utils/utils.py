#!/usr/bin/python

from PIL import Image

#import matplotlib.pyplot as plt
import logging
import optparse, ConfigParser
import sys, os, subprocess, tempfile, cStringIO
from PyQt4 import QtGui,QtCore
#from PySide.QtGui import QImage, QImageReader, QLabel, QPixmap
import ImageQt

import datetime

#try: 
#	import RPi.GPIO as GPIO

#except:
#	print "Try running as sudo... for GPIO library"	

# File photo size settings

class Stri(object):


	def __init__(self):
		self.width = 2592
		self.height = 1944
		self.diskSpaceToReserve = 40 * 1024 * 1024 # Keep 40 mb free on disk
		self.filepath = "/home/pi/LIDAR/images/"

	def write2file(self,hola, nombre):
		if type(hola) == list:
			f = open( nombre +".txt", "w")
			for i in hola:
				f.write(str(i))
				f.write(',')
			f.close()

	# Save a full size image to disk
	def save_image(self, image, filenamePrefix):
		self.keepDiskSpaceFree(self.diskSpaceToReserve)
		time = datetime.datetime.now()
		image.save("imagenes/"+filenamePrefix +"_"+ datetime.datetime.now().ctime() +".jpg")


	#http://www.raspberrypi.org/phpBB3/viewtopic.php?p=358259#p362915
	# Keep free space above given level
	def keepDiskSpaceFree(self,bytesToReserve):
		if (self.getFreeSpace() < bytesToReserve):
			print "out of space"
			sys.exit(1)
			#later i would like to send a message via gsm

	# Get available disk space
	def getFreeSpace(self):
		st = os.statvfs(".")
		du = st.f_bavail * st.f_frsize
		return du

	def capture_image(self):
		width="1280"
		height ="720"
		#raspistill -t 0 (waits forever), 30ms is the minimum time
#   command = "raspistill -w %s -h %s -t 30 -e bmp -o -" % (self.width, self.height)
#		command = "uvccapture -d/dev/video0 -m"
    # StringIO used here as to not wear out the SD card
    # There will be a lot of these pics taken
#		imageData = cStringIO.StringIO()
#		imageData.write(subprocess.check_output(command, shell=True))
#		imageData.seek(0)
#		temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
#    temp_file.write(subprocess.check_output(command, shell=True))
#    temp_file.seek(0)
#    logging.debug("hirez queue push")
		im = Image.open("pics/sa50br50.jpg")
#		im = Image.open("snap.jpg")
#   im = Image.open(imageData)
#		buffer = im.load()
#		im.show()
		return im

	def ccl(self,b_w, th):
		image_pixel = b_w.load()	
		width1, height1 = b_w.size	
		for h in range(height1):
			for w in range(width1):
				pixel = image_pixel[w,h]
				if pixel < th:
					image_pixel[w,h]= 0 #blanco , background
				elif pixel >= th:
					image_pixel[w,h]= 1 #negro

			v = []
			label = 2
			#como mejorar el numero de etiquetas y el valor de equivalencias???
			equivalencias = [0]*300
			image_pixel = b_w.load()
			for h in range(height1):
				for w in range(width1):
					if (w == 0 or h == 0 or w == (width1-1)):
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

						v.append(vecinos)
						
						#si todos mis vecinos son cero y yo soy uno, entonces new label		
						if not vecinos:
							image_pixel[w,h] = label
							label += 1
					
						#sino coloco valor de minimo de los vecinos  						  
						else:				  
							min_vecino = min(vecinos)
#							max_equivalencia = max(vecinos)
							image_pixel[w,h] = min_vecino
						
							#podria revisar si los vecinos son iguales o si solo tengo uno vecino, para no entrar al vector a hacer tonto
							for i in range(len(vecinos)):
								if (equivalencias[vecinos[i]] == 0 or equivalencias[vecinos[i]] > min_vecino):
									equivalencias[vecinos[i]] = min_vecino

		self.write2file(v,"vecinos")
		self.write2file(equivalencias,"equivalencias")
	
	#imagen con min_vecinos o min_labels
		for h in range(height1):
			for w in range(width1):
				#if equivalencias[image_pixel[w,h]] != 0:		
				image_pixel[w,h] = equivalencias[image_pixel[w,h]]

		print "label",label

		return b_w
			
	def get_centroide(self, b_w_c):	
		histo = b_w_c.histogram()
		width1, height1 = b_w_c.size	
		minimo, maximo = b_w_c.getextrema()
		
		self.write2file(histo, "histo")
		print minimo, maximo
		
		blobs = []
		#discriminando segun tamanno del blob
		image_pixel = b_w_c.load()
		for j in range(1,len(histo)):
			#if histo[j]>20 and histo[j]<500:
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
				pfc = round(Centroide_x - ((width1-1)/2.0))
				blobs.append((j, Centroide_x, Centroide_y))
				image_pixel[Centroide_x, Centroide_y] = 0
										
#		b_w.show()
		print blobs
		return b_w_c



def main():
#Ventana
#	app=QtGui.QApplication(sys.argv)
#	pictures=QtGui.QWidget()

#	dato_th=QtGui.QLabel()
#	dato_th.setText("Threshold")
#	dato_th1=QtGui.QLabel()
#	dato_th1.setText("0")

#	dato_label=QtGui.QLabel()
#	dato_label.setText("Label")
#	dato_label1=QtGui.QLabel()
#	dato_label1.setText("0")

#	pic = QtGui.QLabel()
#	#pic.setGeometry(10, 10, 400, 100)
#	pic2 = QtGui.QLabel()
#	pic2.setGeometry(10, 10, 400, 100)

#	layout = QtGui.QVBoxLayout()
#	layout.addWidget(dato_th)
#	layout.addWidget(dato_th1)
#	layout.addWidget(pic)
#	layout.addWidget(dato_label)
#	layout.addWidget(dato_label1)
#	layout.addWidget(pic2)

#	pictures.setLayout(layout)
#	pictures.setWindowTitle("Laser Range Finder")
#	pictures.show()

	stri = Stri()
	x = 1
	try: 	
#		GPIO.setmode(GPIO.BOARD)
#		GPIO.setup(7, GPIO.OUT)

		while(x<2):
#			GPIO.output(7, GPIO.HIGH)
			image = stri.capture_image()
#			GPIO.output(7, GPIO.LOW)
			gray =	image.convert("L")
			
			stri.save_image(gray, "gray")
		 	width, height = gray.size
			b_w = gray.copy()
			b_w.save("b_w.jpg")
		#	b_w = gray.crop((0, 3*height/8, width, (7*height/8)))
#			b_w = gray.crop((0, 6*height/12 - 20, width, (6*height/12) + 20))
			b_w.show()
			
			print "setting pic"
#			qt_bw = ImageQt.ImageQt(b_w)
#			qt_bw1= QtGui.QImage(qt_bw)
#			pic.setPixmap(QtGui.QPixmap(qt_bw1))
			min_value, max_value = b_w.getextrema()
			#Jugar con el threshold
			#th = 3*(max_value - min_value)/4.
			th = 0.88*(max_value - min_value)
			print "th: ", th
#			dato_th1.setText(str(th))
			b_w_c = stri.ccl(b_w, th)
			print "voy por ..."
			stri.get_centroide(b_w_c)
			stri.save_image(b_w_c, "b_w_c")
			b_w_c.show()
			b_w_c.save("b_w_c.jpg")

			#pic2.setPixmap(QtGui.QPixmap("b_w_c.jpg"))
			x +=1
#			dato_label1.setText(str(x))

#		sys.exit(app.exec_())
	except KeyboardInterrupt:
		#GPIO.cleanup()
#		sys.exit(app.exec_())
		sys.exit(1)


if __name__ == '__main__':
	main()

