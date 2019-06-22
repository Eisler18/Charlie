from pyqtgraph.Qt import QtGui, QtCore, uic
#from PyQt4 import uic
import numpy as np 
import pyqtgraph as pg 
import sys
import serial
import math
qtCreatorFile = "osciloscopio.ui" #Importo el archivo de designer

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

	
s = serial.Serial('COM8')
s.baudrate = 115200
s.set_buffer_size(rx_size = 12800)

def serial():	
	channel1 = []
	ndatos = 100
	i = 0
	maximo = 0 #Falta restarle el voltaje DC y dividirlo entre la ganancia
	DC = 1.5

	byte1 = s.read(1) #Lee un byte
	while byte1 >= b'\x80': #Si el byte comienza por 1, vuelve a leer
		byte1 = s.read(1) 
	datos = s.read(299) #Si no comienza por 1, lee el resto de los datos
	
	bandera = (ord(byte1)&64) >> 6
	if bandera:
		channel1.append((((ord(byte1)&63) << 10)|((datos[0]&31) << 5)|(datos[1]&31))*(0.4992/(64*127)))
		rms = ((((((ord(byte1)&63) << 10)|((datos[0]&31) << 5)|(datos[1]&31))*(0.4992/(64*127)))-DC)/31)**2
	else: 
		channel1.append((((ord(byte1)&63) << 10)|((datos[0]&31) << 5)|(datos[1]&31))/64)
		rms = ((((((ord(byte1)&63) << 10)|((datos[0]&31) << 5)|(datos[1]&31))/64)-DC)/31)**2

	for i in range(100): #Decodificacion
		if i != 0:
			bandera = (datos[3*(i-1)+2]&64) >> 6
			if bandera:
				channel1.append((((datos[3*(i-1)+2]&63) << 10)|((datos[3*(i-1)+3]&31) << 5)|(datos[3*(i-1)+4]&31))*(0.4992/(64*127)))
				rms = ((((((datos[3*(i-1)+2]&63) << 10)|((datos[3*(i-1)+3]&31) << 5)|(datos[3*(i-1)+4]&31))*(0.4992/(64*127)))-DC)/31)**2+rms
			else: 
				channel1.append((((datos[3*(i-1)+2]&63) << 10)|((datos[3*(i-1)+3]&31) << 5)|(datos[3*(i-1)+4]&31))/64)
				rms = ((((((datos[3*(i-1)+2]&63) << 10)|((datos[3*(i-1)+3]&31) << 5)|(datos[3*(i-1)+4]&31))/64)-DC)/31)**2+rms
		channeld1=((datos[3*i]) & 64) >> 6
		channeld2=(datos[3*i+1] & 64) >> 6
		
	return channel1, channeld1, channeld2, rms


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		#Inicializar
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		pg.setConfigOptions(foreground='k')
		self.pantalla.setBackground(background='w')
		self.pantalla.setAntialiasing(aa=True)
		self.app=QtGui.QApplication(sys.argv)

		#Variables auxiliares
		self.lectura1 = True
		self.pch1=[]
		self.cont = 0
		self.Maximo = 0
				
		#Crear la ventana de la grafica
		self.traces= dict()
		self.t= np.arange(0, 1, 1/2000)
		n = 1
		m = 1
		axisY = [(0,'0'),(m*1,'1'),(m*2,'2'),(m*3,'3')]
		self.CaxisY = pg.AxisItem(orientation='left')
		self.CaxisY.setTicks([axisY])
		self.Canvas = self.pantalla.addPlot(axisItems={'left':self.CaxisY})
		self.Canvas.showGrid(x=True,y=True, alpha = 0.5)
		self.Canvas.setYRange(0, m*3, 0)
		self.Canvas.setXRange(0, 1*n, 0)
		self.Canvas.hideButtons()
		self.Canvas.invertX(b=True)

		#ESCALA DE VOLT 
		self.PerillaAmp.setTracking(True)
		self.PerillaAmp.valueChanged.connect(self.changebasevolt)

		#ESCALA DE TIEMPO
		self.PerillaTiempo.setTracking(True)
		self.PerillaTiempo.valueChanged.connect(self.changebasetime)

		#DISPLAY 


	def start(self):
		if(sys.flags.interactive != 1) or not hasattr(pg.Qtcore,'graficas'):
			pg.QtGui.QApplication.instance().exec_()
	
	def trace(self,name,dataset_x,dataset_y,color): #Graficar
		if name in self.traces:
			self.traces[name].setData(dataset_x,dataset_y)
		else:
			self.traces[name] = self.Canvas.plot(pen=color) 
			#self.traces[name] = self.Canvas.plot(pen=color,symbolBrush=color,symbolPen=color) #Observar puntos de muestreo

	def update(self): #Actualizar datos
		if self.cont == 6:
			self.cont = 0
		if self.lectura1 == True: #Primera lectura debe leer 10 veces del serial
			i = 0
			for i in range(20):
				ch1, chd1, chd2, rms = serial()
				self.pch1.extend(ch1)
			self.lectura1=False
		else: #Siguientes lecturas: eliminar los 200 datos más viejos y leer nuevos
			del self.pch1[:100]
			ch1, chd1, chd2, rms = serial()
			self.pch1.extend(ch1)


		zero = np.zeros(2000)
		if not chd1:
			self.trace("CH1",self.t,self.pch1,'b')
		#Conversion 
			RMS = ((((rms/100))**(0.5))/0.0063
			#RMS = rms/(100*31*0.0063)
			if self.Maximo < RMS:
				self.Maximo = RMS

		if self.cont == 0:
			if chd2:
				display = self.Maximo
				self.Display.display(display)
				if not chd1:
					self.Maximo = 0
				print(display)
			else: 
				display = 20*math.log10(self.Maximo)   #REVISAR LA CONVERSION
				self.Display.display(display)
				if not chd1:
					self.Maximo = 0
				print(display)
		self.cont = self.cont + 1

		


	def animation(self): #Timer de actualizacion
		timer = QtCore.QTimer()
		timer.timeout.connect(self.update)
		timer.start(45) #De usarse symbolBrush y symbolPen cambiar el tiempo a 0.5 o menos, ya que tarda mucho en graficar y el buffer se llena, sino dejarlo en 90
		self.start()


	#FUNCION PERILLA DE VOLTAJE
	def changebasevolt(self):
		value = self.PerillaAmp.value()
		if value == 1:
			axisY = [(0.9,'0.9'),(1.2,'1.2'),(1.8,'1.8'),(2.1,'2.1')]
			self.CaxisY.setTicks([axisY])
			self.Canvas.setYRange(0.9, 2.1, 0)
		elif value == 2:
			axisY = [(0,'0'),(1,'1'),(2,'2'),(3,'3')]
			self.CaxisY.setTicks([axisY])
			self.Canvas.setYRange(0, 3, 0)
		elif value == 3:
			axisY = [(0,'0'),(3*1,'3'),(3*2,'6'),(3*3,'9')]
			self.CaxisY.setTicks([axisY])
			self.Canvas.setYRange(0, 3*3, 0)

	#FUNCION PERILLA DE TIEMPO
	def changebasetime(self):
		value = self.PerillaTiempo.value()
		if value == 1:
			self.Canvas.setXRange(0, 1, 0)
		elif value == 2:
			n = 1/10
			self.Canvas.setXRange(1-n, 1, 0)
		elif value == 3:
			n = 1/100
			self.Canvas.setXRange(0.998-n, 0.998, 0)
		elif value == 4:
			n = 1/1000
			self.Canvas.setXRange(0.9994-n, 0.9994, 0)


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
	window.show()
	window.animation()
	sys.exit(app.exec_())     