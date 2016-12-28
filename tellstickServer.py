from ctypes import cdll, c_int, c_ubyte, c_void_p, CFUNCTYPE, POINTER, string_at #imports allowing the use of our library
import socket
import json


print "***************"
print "* Serverstart *"
print "***************"

lib = cdll.LoadLibrary('libtelldus-core.so.2') #import our library

def turnOn(uid):
	print("turnOn: " + uid)
	lib.tdTurnOn(uid)

def turnOff(uid):
	print("turnOff: " + uid)
	lib.tdTurnOff(uid)

#function to be called when a device event occurs
def callbackfunction(self, deviceId, method, value, callbackId, context):
	print("callback! " + str(deviceId))

#function to be called when device event occurs, even for unregistered devices
def rawcallbackfunction(self, data, controllerId, callbackId, context):
	print("rawcallbackfunction(data: " + str(data) + ", controllerId: " + str(controllerId) + ")")
	print(string_at(data))

CMPFUNC = CFUNCTYPE(None, c_int, c_int, POINTER(c_ubyte), c_int, c_void_p)
CMPFUNCRAW = CFUNCTYPE(None, POINTER(c_ubyte), c_int, c_int, c_void_p)

cmp_func = CMPFUNC(server.callbackfunction)
cmp_funcraw = CMPFUNCRAW(server.rawcallbackfunction)

lib.tdInit()
lib.tdRegisterDeviceEvent(cmp_func, 0)
lib.tdRegisterRawDeviceEvent(cmp_funcraw, 0) #uncomment this, and comment out tdRegisterDeviceEvent, to see data for not registered devices


TCP_PORT= 5005
BUFFER_SIZE= 200 # Normally 1024, but we want fast response

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(1)
try:
	while 1:
		conn, addr= s.accept()
		print("Connection address: %s" % str(addr))
		while 1:
			data= conn.recv(BUFFER_SIZE)
			if not data: break
			print("received data: %s" % data)
			receivedObject= json.loads(data)
			for key in receivedObject:
				if(key == "msg"):
					print("Message: %s" % receivedObject[key])
				elif(event == "turnOn"):
					turnOn(100)
				elif(event == "turnOff"):
					turnOff(100)
				else:
					print("UNKNOWN: %s: %s" % (key, receivedObject[key]))
			conn.send(data) # echo
		conn.close()
except KeyboardInterrupt:
	print("Keyboard Interrupt")
