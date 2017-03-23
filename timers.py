import socket
import datetime
import time

TCP_IP= '192.168.10.245'#'127.0.0.1'
TCP_PORT= 5005
BUFFER_SIZE= 1024

frUr= datetime.datetime
nodeEvents= []
nodeEvents.append([[1,1,1,1,1,1,1],[19,0],[200],"on"])
nodeEvents.append([[1,1,1,1,1,1,1],[19,30],[100,101],"on"])
nodeEvents.append([[1,1,1,1,0,0,1],[22,0],[200],"off"])
nodeEvents.append([[1,1,1,1,1,1,1],[23,0],[102],"off"])
nodeEvents.append([[1,1,1,1,0,0,1],[23,30],[100,101],"off"])
nodeEvents.append([[0,0,0,0,1,1,0],[23,59],[200],"off"])
nodeEvents.append([[0,0,0,0,0,1,1],[01,00],[100,101],"off"])
#print(frUr.now())
#print(getattr(frUr.now(), 'day'))
#print(frUr.today().weekday())

MESSAGE= '{"event":{"uid":200,"state":"off"}}'
def sendEvent(event):
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(event)
    data= s.recv(BUFFER_SIZE)
    s.close()

    #print("received data: %s" % data)

#sendEvent('{"event":{"uid":102,"state":"off"}}')

#x= 0
while 1:
    print("===== %s =====" % frUr.now())
    for event in nodeEvents:
        #print(frUr.now())
        #print event[3]
        #print frUr.now().hour
        if (event[0][frUr.today().weekday()] and
        event[1][0] == frUr.now().hour and
        event[1][1] == frUr.now().minute):
            for node in event[2]:
                strEvent= "{\"event\":{\"uid\":%i,\"state\":\"%s\"}}"%(node,event[3])
                sendEvent(strEvent)
                #sendEvent('{"event":{"uid":200,"state":"on"}}')
    time.sleep(21)
    #x+=1
    #break;
