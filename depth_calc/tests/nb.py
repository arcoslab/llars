#!/usr/bin/python

from PIL import Image
from PIL import ImageEnhance
import os, sys, cStringIO, subprocess
import pylab
#from scipy import ndimage
#import mahotas, pymorph, scipy
import matplotlib.cm as cm

i=0
pylab.show(block=False)
while i<10:

	###############################
	# Take a picture
	###############################
	wid="1280"
	hei ="720"
	name = "snap_"+str(i)+".jpg"
	#raspistill -t 0 (waits forever), 30ms is the minimum time
	#command = "raspistill -w %s -h %s -t 30 -e bmp -o -" % (width, height)
	command = "uvccapture -d/dev/video1 -x%s -y%s -o%s" %(wid, hei, name)
	# StringIO used here as to not wear out the SD card
	# There will be a lot of these pics taken
	imageData = cStringIO.StringIO()
	imageData.write(subprocess.check_output(command, shell=True))
	imageData.seek(0)
	#im = Image.open("pics/images.jpeg")
	im = Image.open("snap_"+str(i)+".jpg")
	
	pylab.subplot(221)
	pylab.title("Original")
	pylab.imshow(im)
	pylab.draw()

	#im.show()
	###############################
	# Enhance
	###############################
	#converter= ImageEnhance.Color(im)
	#im2 = converter.enhance(3.0)
	#im2.show()

	###############################
	# Convert to gray
	###############################
	gray = im.convert("L")
	pylab.subplot(222)
	pylab.title("Grey")
	pylab.imshow(gray, cmap =cm.Greys_r)
	pylab.draw()
#	gray.show()
	gwidth, gheight = gray.size

	###############################
	# Set threshold
	###############################
	min_max = gray.getextrema()
	print min_max
	th = 0.9*(min_max[1]-min_max[0])
	print th


	###############################
	# Convert to b_w with th
	###############################
	b_w = gray.copy()
	#gray2 = gray.crop((0, 6*gheight/12 - 40, gwidth, (6*gheight/12) + 40))
	#gray2.show()
	#b_w = gray.crop((0, 6*gheight/12 - 80, gwidth, (6*gheight/12) + 80))
	#b_w.show()
	image_pixel = b_w.load()
	width, height = b_w.size
	for h in range(height):
		for w in range(width):
			pixel = image_pixel[w,h]
			if pixel > th:
				image_pixel[w,h]= 255
			elif pixel <= th:
				image_pixel[w,h]= 0

	pylab.subplot(223)
	pylab.title("B_W")
	pylab.imshow(b_w,  cmap =cm.Greys_r)
	pylab.draw()

	#guardamos la nueva imagen
	#save_image(b_w, "b_w")
	#b_w.show()

	Cx = 0
	Cy = 0
	area = 0
	Centroide_x =0
	Centroide_y =0

	image_pixel = b_w.load()
	width, height = b_w.size
	#recorro la matriz
	for h in range(height):   
		for w in range(width):
			if image_pixel[w,h]== 255:
				Cx += w
				Cy +=h
				area += 1

	if area != 0:
		Centroide_x = (Cx/(area*1.0))
		Centroide_y = (Cy/(area*1.0))
		image_pixel[Centroide_x,Centroide_y] = 0
		#b_w.show()
		print "Centroide_x = " , Centroide_x ,  "Centroide_y = " , Centroide_y

	pylab.subplot(224)
	pylab.title("Centroide")
	pylab.imshow(b_w,  cmap =cm.Greys_r)
	pylab.draw()
	
	pylab.show(block=False)
	i+=1
	pylab.savefig("carito.jpg")
#	raw_input("Press enter to continue...")


pylab.show()



