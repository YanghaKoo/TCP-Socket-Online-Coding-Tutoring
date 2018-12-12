import socket
from tkinter import *
from tkinter.ttk import *


host = ''
port = 4000


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((host, port))
  s.listen(1)
  conn, addr = s.accept()

  while True:
    data = conn.recv(1024)
    if not data: break
    print(data.decode())
    conn.sendall(data)
  conn.close()




