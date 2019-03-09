def numdatos():
	ndatos = 2000
	return ndatos

def serial():
	import serial
	
	s = serial.Serial('COM8')
	s.baudrate = 115200
	channel1 = []
	channel2 = []
	channeld1 = []
	channeld2 = []
	ndatos = 2000
	i = 0

	byte1 = s.read(1)
	while byte1 > b'\x80':
		byte1 = s.read(1) 
	datos = s.read(7999)

	channel1.append(((ord(byte1) << 6)|(datos[0] & 63))/1024)

	for i in range(ndatos-1):
		channel1.append(((datos[4*i+3] << 6)|(datos[4*i+4] & 63))/1024)
	i = 0

	for i in range(ndatos):
		channeld1.append(((datos[4*i]) & 64) >> 6)
		channeld2.append((datos[4*i+1] & 64) >> 6)
		channel2.append((((datos[4*i+1] & 63) << 6)|(datos[4*i+2] & 63))/1024)
		
		"""print('Canal digital 1',channeld1)
		print('Canal digital 2',channeld2)
		print('Canal 1',channel1)
		print('Canal 2',channel2)"""
	return channel1, channel2, channeld1, channeld2