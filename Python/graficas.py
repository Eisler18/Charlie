from pyqtgraph.Qt import QtGui, QtCore
import numpy as np 
import pyqtgraph as pg 
import sys
import serial
	
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


class plot(object):
	def __init__(self):
		self.c1 = True
		self.c2 = True
		self.cd1 = True
		self.cd2 = True
		self.lectura1 = True
		self.pch1=[]
		self.pch2=[]
		self.pchd1=[]
		self.pchd2=[]

		self.traces= dict()
		self.t= np.arange(0, 1, 1/2000)
		pg.setConfigOptions(antialias=True)
		self.app=QtGui.QApplication(sys.argv)
		self.win=pg.GraphicsWindow()
		self.win.resize(1000,600)
		self.win.setWindowTitle('pyqtgraph example')
		n = 1
		m = 1
		axisY = [(0,'0'),(m*1,'1'),(m*2,'2'),(m*3,'3'),(m*4,'4')]
		self.CaxisY = pg.AxisItem(orientation='left')
		self.CaxisY.setTicks([axisY])
		self.Canvas = self.win.addPlot(row=0,col=0,colspan=4,title="Osciloscopio",axisItems={'left':self.CaxisY})
		self.Canvas.showGrid(x=True,y=True, alpha = 0.5)
		self.Canvas.setYRange(0, m*4, 0)
		self.Canvas.setXRange(0, 1*n, 0)
		self.Canvas.hideButtons()
		self.Canvas.invertX(b=True)

		#BOTONES
		#Botones de Amplitud
		proxy1 = QtGui.QGraphicsProxyWidget()
		button1 = QtGui.QPushButton('0.3 V/div')
		proxy1.setWidget(button1)
		self.V03 = self.win.addLayout(row=3, col=1)
		self.V03.addItem(proxy1,row=0,col=0)
		button1.clicked.connect(self.Vt03)

		proxy2 = QtGui.QGraphicsProxyWidget()
		button2 = QtGui.QPushButton('1 V/div')
		proxy2.setWidget(button2)
		self.V1 = self.win.addLayout(row=3, col=2)
		self.V1.addItem(proxy2,row=0,col=0)
		button2.clicked.connect(self.Vt1)

		proxy3 = QtGui.QGraphicsProxyWidget()
		button3 = QtGui.QPushButton('3 V/div')
		proxy3.setWidget(button3)
		self.V3 = self.win.addLayout(row=3, col=3)
		self.V3.addItem(proxy3,row=0,col=0)
		button3.clicked.connect(self.Vt3)

		#Botones de frecuencia
		proxy4 = QtGui.QGraphicsProxyWidget()
		button4 = QtGui.QPushButton('10 Hz')
		proxy4.setWidget(button4)
		self.f10 = self.win.addLayout(row=4, col=1)
		self.f10.addItem(proxy4,row=0,col=0)
		button4.clicked.connect(self.fq10)

		proxy5 = QtGui.QGraphicsProxyWidget()
		button5 = QtGui.QPushButton('100 Hz')
		proxy5.setWidget(button5)
		self.f100 = self.win.addLayout(row=4, col=2)
		self.f100.addItem(proxy5,row=0,col=0)
		button5.clicked.connect(self.fq100)

		proxy6 = QtGui.QGraphicsProxyWidget()
		button6 = QtGui.QPushButton('1 kHz')
		proxy6.setWidget(button6)
		self.f1k = self.win.addLayout(row=4, col=3)
		self.f1k.addItem(proxy6,row=0,col=0)
		button6.clicked.connect(self.fq1k)

		proxy11 = QtGui.QGraphicsProxyWidget()
		button11 = QtGui.QPushButton('1 Hz')
		proxy11.setWidget(button11)
		self.f1 = self.win.addLayout(row=2, col=2)
		self.f1.addItem(proxy11,row=0,col=0)
		button11.clicked.connect(self.fq1)

		"""self.label1=self.win.addLayout(row=1,col=2)
		self.label1.addLabel(text='Selector de Canales',row=0,col=0)

		self.label2=self.win.addLayout(row=3,col=0)
		self.label2.addLabel(text='Selector de Amplitud',row=0,col=0)

		self.label3=self.win.addLayout(row=4,col=0)
		self.label3.addLabel(text='Selector de base de tiempo',row=0,col=0)"""

		#Botones de canales
		proxy7 = QtGui.QGraphicsProxyWidget()
		button7 = QtGui.QPushButton('Channel 1')
		proxy7.setWidget(button7)
		self.channel1 = self.win.addLayout(row=1, col=1)
		self.channel1.addItem(proxy7,row=0,col=0)
		button7.clicked.connect(self.chn1)

		proxy8 = QtGui.QGraphicsProxyWidget()
		button8 = QtGui.QPushButton('Channel 2')
		proxy8.setWidget(button8)
		self.channel2 = self.win.addLayout(row=1, col=3)
		self.channel2.addItem(proxy8,row=0,col=0)
		button8.clicked.connect(self.chn2)

		proxy9 = QtGui.QGraphicsProxyWidget()
		button9 = QtGui.QPushButton('ChannelD 1')
		proxy9.setWidget(button9)
		self.channeld1 = self.win.addLayout(row=2, col=1)
		self.channeld1.addItem(proxy9,row=0,col=0)
		button9.clicked.connect(self.chnd1)

		proxy10 = QtGui.QGraphicsProxyWidget()
		button10 = QtGui.QPushButton('ChannelD 2')
		proxy10.setWidget(button10)
		self.channeld2 = self.win.addLayout(row=2, col=3)
		self.channeld2.addItem(proxy10,row=0,col=0)
		button10.clicked.connect(self.chnd2)

	#FUNCIONES DE AMPLITUD
	def Vt03(self):
		axisY = [(0,'0'),(0.3*1,'0.3'),(0.3*2,'0.6'),(0.3*3,'0.9'),(0.3*4,'1.2')]
		self.CaxisY.setTicks([axisY])
		self.Canvas.setYRange(0, 0.3*4, 0)
	def Vt1(self):
		axisY = [(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4')]
		self.CaxisY.setTicks([axisY])
		self.Canvas.setYRange(0, 4, 0)
	def Vt3(self):
		axisY = [(0,'0'),(3*1,'3'),(3*2,'6'),(3*3,'9'),(3*4,'12')]
		self.CaxisY.setTicks([axisY])
		self.Canvas.setYRange(0, 3*4, 0)

	#FUNCIONES DE FRECUENCIA
	def fq10(self):
		n = 1/10
		self.Canvas.setXRange(0, 1*n, 0)
	def fq100(self):
		n = 1/100
		self.Canvas.setXRange(0, 1*n, 0)
	def fq1k(self):
		n = 1/1000
		self.Canvas.setXRange(0, 1*n, 0)
	def fq1(self):
		n = 1
		self.Canvas.setXRange(0, 1*n, 0)

	#FUNCIONES CANALES
	def chn1(self):
		if self.c1 == True:
			self.c1 = False
		else:
			self.c1 = True
	def chn2(self):
		if self.c2 == True:
			self.c2 = False
		else:
			self.c2 = True
	def chnd1(self):
		if self.cd1 == True:
			self.cd1 = False
		else:
			self.cd1 = True
	def chnd2(self):
		if self.cd2 == True:
			self.cd2 = False
		else:
			self.cd2 = True



	def start(self):
		if(sys.flags.interactive != 1) or not hasattr(pg.Qtcore,'graficas'):
			pg.QtGui.QApplication.instance().exec_()
	
	def trace(self,name,dataset_x,dataset_y,color):
		if name in self.traces:
			self.traces[name].setData(dataset_x,dataset_y)
		else:
			self.traces[name] = self.Canvas.plot(pen=color)#,symbolBrush=color,symbolPen=color)

	def update(self):
		if self.lectura1 == True:
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
			self.trace("CH1",self.t,self.pch1,'y')
		else:
			self.trace("CH1",self.t,zero,'k')
		if self.c2 == True:
			self.trace("CH2",self.t,self.pch2,'r')
		else:
			self.trace("CH2",self.t,zero,'k')
		if self.cd1 == True:
			self.trace("CHD1",self.t,self.pchd1,'y')
		else:
			self.trace("CHD1",self.t,zero,'k')
		if self.cd2 == True:
			self.trace("CHD2",self.t,self.pchd2,'r')
		else:
			self.trace("CHD2",self.t,zero,'k')
		
	def animation(self):
		timer = QtCore.QTimer()
		timer.timeout.connect(self.update)
		timer.start(90) #De usarse symbolBrush y symbolPen cambiar el tiempo a 0.5 o menos, ya que tarda mucho en graficar y el buffer se llena, sino dejarlo en 90
		self.start()

if __name__ == '__main__':
	p = plot()
	p.animation()

