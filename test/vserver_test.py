# Echo server program
import socket
import pyaudio
import wave
import time

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
RECORD_SECONDS = 4000


HOST = '192.168.0.18'   #여기다가도 내 흰색노트북 아이피 쳐줘야함
PORT = 50007              # Arbitrary non-privileged port


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)


#connection setup done and client connected.



p = pyaudio.PyAudio()

# for receiving data
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

# for sending data
stream2 = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


data='a'
i=0
while data != '':
    try:			# receiving data
        data = conn.recv(1024)
        stream.write(data)
        print(i)
        i=i+1
    except KeyboardInterrupt:
     	break
    except:
        pass

    try:		# sending data
        data2  = stream2.read(CHUNK)
        conn.sendall(data2)
    except KeyboardInterrupt:
     	break
    except:
        pass




stream.stop_stream()
stream.close()
p.terminate()
conn.close()
