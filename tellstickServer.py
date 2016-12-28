import socket
import json

TCP_IP= '127.0.0.1'
TCP_PORT= 5005
BUFFER_SIZE= 200 # Normally 1024, but we want fast response

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
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
				else:
					print("UNKNOWN: %s: %s" % (key, receivedObject[key]))
			conn.send(data) # echo
		conn.close()
except KeyboardInterrupt:
	print("Keyboard Interrupt")
