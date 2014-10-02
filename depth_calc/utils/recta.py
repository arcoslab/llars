#!/usr/bin/python

import math

def recta(par1, par2):
#par = (distancia, pfc)	
#distancia = m pfc + b
#m = distancia2 - distancia1 / pfc2 - pfc1		
	m = (par2[0]- par1[0])/((par2[1] - par1[1])*1.0)
	b = par1[0] - m * par1[1]
	m_b = m,b	
	return m_b
	
def write2file(hola, nombre):
	if type(hola) == list:
		f = open( nombre +".txt", "w")
		for i in hola:
			f.write(str(i))
			f.write('\n')
		f.close()

#Calbracion 1 (distancia, pfc), distancia entre camara y laser aproximadamente 12 cm
#datos=[(distancia, pfc)]
datos = [(30,-77), (35, -58), (40,-51), (45,-37), (50,-28), (55	,-19), (60	,-13),(65,-5),(70, 2),(75,4),(80, 5),(85,9.5),(90,14),(95,16),(100,19.5),(105,20),(110,21),(115,23.5),(120,24),(125,26.6666666667),(130,27.5),(140,30),(145,31),(150,32),(155,33),(160,34),(165,35),(210,41)]

m_bs = []
i = 0
while i < len(datos)-1:
	m_b = recta(datos[i],datos[i+1])
	m_bs.append(m_b)
	i+=1

print m_bs	
write2file(m_bs, "m_bs")


def distance(pfc):
	global medidas
	global pfcs
	global m_bs
	i = 0
	while(i < len(pfcs)):
		if pfc > pfcs[i]:
			i +=1
			#print "i",i
			if i >= len(pfcs):
				print "fuera del alcance de medicion"
								
		else:
			print"pfc", pfc, "i = ", i, "m =" , m_bs[i-1][0], "b =" , m_bs[i-1][1]
			distancia = m_bs[i-1][0]* pfc + m_bs[i-1][1]
			i = len(pfcs)
			print "distancia",distancia
			medidas.append((distancia, pfc))

