from ctypes import cdll, c_int, c_ubyte, c_void_p, CFUNCTYPE, POINTER, string_at #imports allowing the use of our library
import socket
import json


print "***************"
print "* Serverstart *"
print "***************"

lib = cdll.LoadLibrary('libtelldus-core.so.2') #import our library
states= {}

def turnOn(uid):
	print("turnOn: " + str(uid))
	states[uid]= True
	lib.tdTurnOn(uid)

def turnOff(uid):
	print("turnOff: " + str(uid))
	states[uid]= False
	lib.tdTurnOff(uid)

#function to be called when a device event occurs
def callbackfunction(deviceId, method, value, callbackId, context):
	print("callback! " + str(deviceId) + ": " + str(method))

	#LivingRoom_Switch
	if (deviceId == 199):
		if (method == 1):
			try:
				if (states[102]):#Pixarlamp
					print "if 1"
					#self.turnOn(taklampa)
			except Exception, e:
				print "Exception(on)1: ", e
			try:
				if (states[100] and states[101]):
					print "if 2"
					turnOn(102)
			except Exception, e:
				print "Exception(on)2: ", e
			turnOn(100)
			turnOn(101)
		elif (method == 2):
			try:
				if (not states[102]):
					print "if 11"
					turnOff(100)
					turnOff(101)
			except Exception, e:
				print "Exception(off): ", e
				pass
			turnOff(102)
		return

	#Bedroom Remote Controll
	#Button 1
	if (deviceId == 499):
		if (method == 1):
			turnOn(200)
		elif (method == 2):
			turnOff(200)
		return
	#Button 2
	if (deviceId == 498):
		if (method == 1):
			pass
		elif (method == 2):
			pass
		return
	#Button 3
	if (deviceId == 497):
		if (method == 1):
			turnOn(400)
		elif (method == 2):
			turnOff(400)
		return

#function to be called when device event occurs, even for unregistered devices
def rawcallbackfunction(data, controllerId, callbackId, context):
	print("rawcallbackfunction(data: " + str(data) + ", controllerId: " + str(controllerId) + ")")
	print(string_at(data))

CMPFUNC = CFUNCTYPE(None, c_int, c_int, POINTER(c_ubyte), c_int, c_void_p)
CMPFUNCRAW = CFUNCTYPE(None, POINTER(c_ubyte), c_int, c_int, c_void_p)

cmp_func = CMPFUNC(callbackfunction)
cmp_funcraw = CMPFUNCRAW(rawcallbackfunction)

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
				elif(key == "event"):
					if(receivedObject[key]["state"] == "on"):
						turnOn(receivedObject[key]["uid"])
					elif(receivedObject[key]["state"] == "off"):
						turnOff(receivedObject[key]["uid"])
				else:
					print("UNKNOWN: %s: %s" % (key, receivedObject[key]))
			conn.send(data) # echo
		conn.close()
except KeyboardInterrupt:
	print("Keyboard Interrupt")
