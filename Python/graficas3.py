from pyqtgraph.Qt import QtGui, QtCore, uic
#from PyQt4 import uic
import numpy as np 
import pyqtgraph as pg 
import sys
import serial
qtCreatorFile = "osciloscopio.ui" #Importo el archivo de designer

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

	
s = serial.Serial('COM8')
s.baudrate = 115200
s.set_buffer_size(rx_size = 12800)

def serial():	
	channel1 = []
	channel2 = []
	channeld1 = []
	channeld2 = []
	ndatos = 200
	i = 0

	byte1 = s.read(1)
	while byte1 > b'\x80':
		byte1 = s.read(1) 
	datos = s.read(799)
	
	channel1.append(((ord(byte1) << 6)|(datos[0] & 63))/1024)

	for i in range(200):
		if i != 0:
			channel1.append(((datos[4*(i-1)+3] << 6)|(datos[4*(i-1)+4] & 63))/1024)
		channeld1.append(((datos[4*i]) & 64) >> 6)
		channeld2.append((datos[4*i+1] & 64) >> 6)
		channel2.append((((datos[4*i+1] & 63) << 6)|(datos[4*i+2] & 63))/1024)

	#buf = str(s.in_waiting)
	#print(buf)
	return channel1, channel2, channeld1, channeld2


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		pg.setConfigOptions(foreground='k')
		self.pantalla.setBackground(background='w')
		self.pantalla.setAntialiasing(aa=True)
		self.app=QtGui.QApplication(sys.argv)
		
		self.c1 = True        #Habilita los 4 canales y despues habilita la lectura de datos
		self.c2 = True
		self.cd1 = True
		self.cd2 = True
		self.lectura1 = True
		self.pch1=[]
		self.pch2=[]
		self.pchd1=[]
		self.pchd2=[]
		
		#self.win=pg.GraphicsWindow()
		#self.pantalla.resize(550,250)
		#self.win.setWindowTitle('pyqtgraph example')
		self.traces= dict()                                    #Creacion y definicion de los ejes
		self.t= np.arange(0, 1, 1/2000)
		n = 1
		m = 1
		axisY = [(0,'0'),(m*1,'1'),(m*2,'2'),(m*3,'3'),(m*4,'4')]
		self.CaxisY = pg.AxisItem(orientation='left')
		self.CaxisY.setTicks([axisY])
		self.Canvas = self.pantalla.addPlot(axisItems={'left':self.CaxisY})
		self.Canvas.showGrid(x=True,y=True, alpha = 0.5)
		self.Canvas.setYRange(0, m*4, 0)
		self.Canvas.setXRange(0, 1*n, 0)
		self.Canvas.hideButtons()
		self.Canvas.invertX(b=True)


		#Escala de volt          
		self.PerillaAmp.setTracking(True)                           #Cada vez que se mueva la perilla entra en la funcion respectiva
		self.PerillaAmp.valueChanged.connect(self.changebasevolt)

		#Escala de tiempo
		self.PerillaTiempo.setTracking(True)
		self.PerillaTiempo.valueChanged.connect(self.changebasetime)

		#Seleccion de canales 
		self.Canal1.stateChanged.connect(self.cha1)                #Encedido y apagado de los canales
		self.Canal2.stateChanged.connect(self.cha2)
		#Canales Digitales
		self.Canaldig1.stateChanged.connect(self.chd1)
		self.Canaldig2.stateChanged.connect(self.chd2)

	def start(self):
		if(sys.flags.interactive != 1) or not hasattr(pg.Qtcore,'graficas'):
			pg.QtGui.QApplication.instance().exec_()
	
	def trace(self,name,dataset_x,dataset_y,color):
		if name in self.traces:
			self.traces[name].setData(dataset_x,dataset_y)
		else:
			self.traces[name] = self.Canvas.plot(pen=color)#,symbolBrush=color,symbolPen=color)

	def update(self):                            
		if self.lectura1 == True:            #Bucle para la lectura de los datos                    
			i = 0
			for i in range(10):
				ch1, ch2, chd1, chd2 = serial()
				self.pch1.extend(ch1)
				self.pch2.extend(ch2)
				self.pchd1.extend(chd1)
				self.pchd2.extend(chd2)
			self.lectura1=False
		else:
			del self.pch1[:200]
			del self.pch2[:200]
			del self.pchd1[:200]
			del self.pchd2[:200]
			ch1, ch2, chd1, chd2 = serial()
			self.pch1.extend(ch1)
			self.pch2.extend(ch2)
			self.pchd1.extend(chd1)
			self.pchd2.extend(chd2)

		zero = np.zeros(2000)
		if self.c1 == True:
			self.trace("CH1",self.t,self.pch1,'b')
		else:
			self.trace("CH1",self.t,zero,'w')
		if self.c2 == True:
			self.trace("CH2",self.t,self.pch2,'r')
		else:
			self.trace("CH2",self.t,zero,'w')
		if self.cd1 == True:
			self.trace("CHD1",self.t,self.pchd1,'b')
		else:
			self.trace("CHD1",self.t,zero,'w')
		if self.cd2 == True:
			self.trace("CHD2",self.t,self.pchd2,'r')
		else:
			self.trace("CHD2",self.t,zero,'w')
		
	def animation(self):
		timer = QtCore.QTimer()
		timer.timeout.connect(self.update)
		timer.start(90) #De usarse symbolBrush y symbolPen cambiar el tiempo a 0.5 o menos, ya que tarda mucho en graficar y el buffer se llena, sino dejarlo en 90
		self.start()


	def changebasevolt(self):                         #Funciones para los botones 
		value = self.PerillaAmp.value()
		if value == 1:
			axisY = [(0,'0'),(0.3*1,'0.3'),(0.3*2,'0.6'),(0.3*3,'0.9'),(0.3*4,'1.2')]
			self.CaxisY.setTicks([axisY])
			self.Canvas.setYRange(0, 0.3*4, 0)
		elif value == 2:
				axisY = [(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4')]
				self.CaxisY.setTicks([axisY])
				self.Canvas.setYRange(0, 4, 0)
		elif value == 3:
				axisY = [(0,'0'),(3*1,'3'),(3*2,'6'),(3*3,'9'),(3*4,'12')]
				self.CaxisY.setTicks([axisY])
				self.Canvas.setYRange(0, 3*4, 0)

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


	#FUNCIONES DE CANALES
	def cha1(self,state):
		if state == QtCore.Qt.Checked:
			if self.c1 == True:
				self.c1 = False
		else:
			self.c1 = True

	def cha2(self,state):
		if state == QtCore.Qt.Checked:
			if self.c2 == True:
				self.c2 = False
		else:
			self.c2 = True

	def chd1(self,state):
		if state == QtCore.Qt.Checked:
			if self.cd1 == True:
				self.cd1 = False
		else:
			self.cd1 = True

	def chd2(self,state):
		if state == QtCore.Qt.Checked:
			if self.cd2 == True:
				self.cd2 = False
		else: 
			self.cd2 = True


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
	window.show()
	window.animation()
	sys.exit(app.exec_())     
