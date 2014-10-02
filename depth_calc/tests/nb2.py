#!/usr/bin/python

import numpy as np
import scipy
import pylab
import pymorph
import mahotas
from scipy import ndimage

import os, sys, cStringIO, subprocess

i=0

pylab.show(block=False)
while i<2:

	###############################
	# Take a picture
	###############################
	wid="1280"
	hei ="720"
	name = "snap_"+str(i)+".jpg"
	#raspistill -t 0 (waits forever), 30ms is the minimum time
	#command = "raspistill -w %s -h %s -t 30 -e bmp -o -" % (width, height)
	command = "uvccapture -d/dev/video0 -x%s -y%s -o%s" %(wid, hei, name)
	imageData = cStringIO.StringIO()
	imageData.write(subprocess.check_output(command, shell=True))
	imageData.seek(0)

	#http://pythonvision.org/basic-tutorial
	#http://mahotas.readthedocs.org/en/latest/labeled.html#labeling-images

	im = mahotas.imread("snap_"+str(i)+".jpg")

	pylab.subplot(221)
	pylab.imshow(im)
	pylab.gray()
	#T = 0.5*(im.max()-im.min())
	imf = ndimage.gaussian_filter(im, 8)
	T = mahotas.thresholding.otsu(imf)
	#T = 0.5*(im.max()-im.min())
	print "T: ", T
	pylab.subplot(222)
	pylab.imshow(imf>T)
	#pylab.show()

#	labeled,nr_objects = ndimage.label(imf > T)
#	print nr_objects
#	pylab.subplot(223)
#	pylab.imshow(labeled)
#	pylab.jet()
	#pylab.show()

#	dnaf = ndimage.gaussian_filter(im, 16)
##	rmax = pymorph.regmax(dnaf)
#	pylab.imshow(dnaf>T)
#	pylab.subplot(224)
##	pylab.imshow(pymorph.overlay(im, rmax))


	pylab.show(block=False)
	pylab.draw()
	i+=1
	raw_input("Press enter to continue...")

#pylab.show()
