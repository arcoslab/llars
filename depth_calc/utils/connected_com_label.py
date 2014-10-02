def Connected_com_label(b_w1):

width, height = b_w1.size
image_pixel = b_w1.load()
for h in range(height):
	for w in range(width):
	#Blanco va a ser 0, negro 1
		if image_pixel[w,h] == 255:
			image_pixel[w,h] = 0
		else:
			image_pixel[w,h] = 1						
			
b_w1.show("0y1")

v = []
label = 2
equivalencias = [0]*500
image_pixel = b_w1.load()
for h in range(height):
	for w in range(width):
		if (w == 0 or h == 0 or w == (width-1)):
			pass
					
		else:
			#si no es blanco
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
		
#				print vecinos
					
				v.append(vecinos)
				
				if not vecinos:
					image_pixel[w,h] = label
					label += 1
				
				  
				else:				  
					min_equivalencia = min(vecinos)
					max_equivalencia = max(vecinos)
					image_pixel[w,h] = min_equivalencia
					
					for i in range(len(vecinos)):
						if (equivalencia[vecinos[i]] == 0 or equivalencia[vecinos[i]] > min_equivalencia):
							equivalencia[vecinos[i]] = min_equivalencia
	
for h in range(height):
	for w in range(width):
		image_pixel[w,h] = equivalencia[image_pixel[w,h]]

		print "Connected component"
										
	return b_w1						

