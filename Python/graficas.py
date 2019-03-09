from pyqtgraph.Qt import QtGui, QtCore
import numpy as np 
import pyqtgraph as pg 
import sys
import Serial 

class plot(object):
	def __init__(self):
		self.c1 = True
		self.c2 = True
		self.cd1 = True
		self.cd2 = True
		self.traces= dict()
		self.t= np.arange(0, 3, 3/Serial.numdatos())
		pg.setConfigOptions(antialias=True)
		self.app=QtGui.QApplication(sys.argv)
		self.win=pg.GraphicsWindow()
		self.win.resize(1000,600)
		self.win.setWindowTitle('pyqtgraph example')
		n = 1/10 
		axisX = [(n*0.33,' '),(n*0.66,' '),(n*1,' '),(n*1.33,' '),(n*1.66,' '),
				(n*2,' '),(n*2.33,' '),(n*2.66,' '),(n*3,' ')]
		""",(n*2,' '),
		(n*2.2,' '),(n*2.4,' '),(n*2.6,' '),(n*2.8,' '),(n*3,'seg')]"""
		self.CaxisX = pg.AxisItem(orientation='bottom')
		self.CaxisX.setTicks([axisX])
		m = 1
		axisY = [(0,' '),(m*1,' '),(m*2,' '),(m*3,' '),(m*4,'V')]
		self.CaxisY = pg.AxisItem(orientation='left')
		self.CaxisY.setTicks([axisY])
		self.Canvas = self.win.addPlot(row=0,col=0,colspan=4,title="Osciloscopio",axisItems={'bottom':self.CaxisX, 'left':self.CaxisY})
		self.Canvas.showGrid(x=True,y=True, alpha = 0.5)
		self.Canvas.setYRange(0, m*4, 0)
		self.Canvas.setXRange(0, 3*n, 0)
		self.Canvas.hideButtons()

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

		

		self.label1=self.win.addLayout(row=1,col=2,rowspan=2)
		self.label1.addLabel(text='Selector de Canales',row=0,col=0)

		"""self.label2=self.win.addLayout(row=3,col=0)
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
		axisY = [(0,' '),(0.3*1,' '),(0.3*2,' '),(0.3*3,' '),(0.3*4,'V')]
		self.CaxisY.setTicks([axisY])
		self.Canvas.setYRange(0, 0.3*4, 0)
	def Vt1(self):
		axisY = [(0,' '),(1,' '),(2,' '),(3,' '),(4,'V')]
		self.CaxisY.setTicks([axisY])
		self.Canvas.setYRange(0, 4, 0)
	def Vt3(self):
		axisY = [(0,' '),(3*1,' '),(3*2,' '),(3*3,' '),(3*4,'V')]
		self.CaxisY.setTicks([axisY])
		self.Canvas.setYRange(0, 3*4, 0)

	#FUNCIONES DE FRECUENCIA
	def fq10(self):
		n = 1/10
		axisX = [(n*0.2,' '),(n*0.4,' '),(n*0.6,' '),(n*0.8,' '),(n*1,' '),
				(n*1.2,' '),(n*1.4,' '),(n*1.6,' '),(n*1.8,' '),(n*2,' '),
				(n*2.2,' '),(n*2.4,' '),(n*2.6,' '),(n*2.8,' '),(n*3,'seg')]
		self.CaxisX.setTicks([axisX])
		self.Canvas.setXRange(0.2*n, 3*n, 0)
	def fq100(self):
		n = 1/100
		axisX = [(n*0.2,' '),(n*0.4,' '),(n*0.6,' '),(n*0.8,' '),(n*1,' '),
				(n*1.2,' '),(n*1.4,' '),(n*1.6,' '),(n*1.8,' '),(n*2,' '),
				(n*2.2,' '),(n*2.4,' '),(n*2.6,' '),(n*2.8,' '),(n*3,'seg')]
		self.CaxisX.setTicks([axisX])
		self.Canvas.setXRange(0.2*n, 3*n, 0)
	def fq1k(self):
		n = 1/1000
		axisX = [(n*0.2,' '),(n*0.4,' '),(n*0.6,' '),(n*0.8,' '),(n*1,' '),
				(n*1.2,' '),(n*1.4,' '),(n*1.6,' '),(n*1.8,' '),(n*2,' '),
				(n*2.2,' '),(n*2.4,' '),(n*2.6,' '),(n*2.8,' '),(n*3,'seg')]
		self.CaxisX.setTicks([axisX])
		self.Canvas.setXRange(0.2*n, 3*n, 0)

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
	

# if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        #pg.QtGui.QApplication.exec_()

	def trace(self,name,dataset_x,dataset_y,color):
		if name in self.traces:
			self.traces[name].setData(dataset_x,dataset_y)
		else:
			self.traces[name] = self.Canvas.plot(pen=pg.mkPen(color))

	def update(self):
		ch1, ch2, chd1, chd2 = Serial.serial()
		zero = np.zeros(Serial.numdatos())
		if self.c1 == True:
			self.trace("CH1",self.t,ch1,'y')
		else:
			self.trace("CH1",self.t,zero,'k')
		if self.c2 == True:
			self.trace("CH2",self.t,ch2,'r')
		else:
			self.trace("CH2",self.t,zero,'k')
		if self.cd1 == True:
			self.trace("CHD1",self.t,chd1,'y')
		else:
			self.trace("CHD1",self.t,zero,'k')
		if self.cd2 == True:
			self.trace("CHD2",self.t,chd2,'r')
		else:
			self.trace("CHD2",self.t,zero,'k')
		
	def animation(self):
		timer = QtCore.QTimer()
		timer.timeout.connect(self.update)
		timer.start(500)
		self.start()

if __name__ == '__main__':
	p = plot()
	p.animation()

