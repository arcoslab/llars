#!/usr/bin/python

from PIL import Image
import os, sys

#importing RPi.GPIO library
#try: 
#	import RPi.GPIO as GPIO
#except:
#	print "Try running as sudo... for GPIO library"	

#set pin mode 	
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7, GPIO.OUT)


def main():
	try:
		x = 0
		go = True
		while(go):
			#turn pin on, take picture and turn it off
			#GPIO.output(7, GPIO.HIGH)
			os.system('uvccapture -d/dev/video0 -x1280 -y720')
			#os.system('raspistill -w 1280 -h 720 -t 30 -tl 0 -o snap.jpg -n')
			#GPIO.output(7, GPIO.LOW)
			image = Image.open('snap.jpg')
			image.save("test_"+ str(x) +".jpg")
			x += 1
			command = str(raw_input("If you want to continue, then write go, else write no:"))
		
			if command == "go":
				go = True
			else:
				go = False
		
		image.show()				
		#GPIO.cleanup()
		sys.exit(1)

	except KeyboardInterrupt:
		#GPIO.cleanup()
		sys.exit(1)


if __name__ == '__main__':
	main()
