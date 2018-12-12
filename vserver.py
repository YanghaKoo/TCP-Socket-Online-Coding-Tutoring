import socket
import pyaudio
import wave
import time

def main(port):
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 20000
    RECORD_SECONDS = 4000

    HOST = ''        
    PORT = port 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)

    p = pyaudio.PyAudio()

    #recv
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    #send
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
            if i == 1: print("voice call connected")
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


if __name__ == '__main__':
    main(50007)