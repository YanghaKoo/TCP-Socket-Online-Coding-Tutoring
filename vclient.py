import socket
import pyaudio
import wave

def main(port):
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 20000

    HOST = '127.0.0.1'
    PORT = port       

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    p = pyaudio.PyAudio()

    #send
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    #recv
    stream2 = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)



    data2='a'

    i=0
    while data2 != '':
        try:		
            data  = stream.read(CHUNK)
            s.sendall(data)
        except KeyboardInterrupt:
            break
        except:
            pass

        try:       	# receiving data
            data2 = s.recv(1024)
            stream2.write(data2)
            if i == 1: print("voice call connected")
            i=i+1
        except KeyboardInterrupt:
            break
        except:
            pass

    print("*done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    s.close()

    print("*closed")

if __name__ == '__main__':
    main(50007)
