from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from getpass import getpass
import editorS
import editorT
import vserver
import vclient
import sys

def receive(address):        
  while True:
    try:          
      msg = client_socket.recv(BUFSIZ).decode("utf8")                              
      splited = msg.split()      
      name = splited[0]
      print('')
      if name != 'failure':
        print("logged in user : " + name)

      if name == 'javascript' or name == 'python':              
        print('Tutor logged in')
        mode = "T"  
      elif name == 'failure' or name =='duplicate':
        print('login failed!')
        mode = "failed"
        client_socket.send(bytes("error", "utf8"))
      else : 
        print('Student logged in')
        mode = "S"                        

      # 학생 로그인 case
      if mode == "S":        
        print('')
        print('현재 수업 가능한 선생님은 ')
        tutorList = []
        for idx in splited:
          if idx != name:              
            print(idx)
            tutorList.append(idx)
        if len(tutorList) == 0 :
          print("없습니다.")
          client_socket.send(bytes(id, "utf8"))
          quit()
        else :  
          print("입니다.")
          selected = input('어떤 선생님의 수업을 들으시겠습니까? : ')                                                  
          
          port = 0
          vport = 0
          if selected == "javascript":      
            port = 4000
            client_socket.send(bytes(selected, "utf8"))
            
            # 통화 클라
            vport = 50007
            Thread(target=vclient.main, args=(vport,)).start()

          elif selected == "python":            
            port = 5000
            client_socket.send(bytes(selected, "utf8"))
            
            # 통화 클라
            vport = 50008
            Thread(target=vclient.main, args=(vport,)).start()
          else :
            print("잘못 입력하셨습니다.")
            client_socket.send(bytes(id, "utf8"))
            quit()          
          #print(port)
          root = Tk()
          root.resizable(False, False)
          root.geometry("765x580+100+100")      
          
          app = editorS.MyFrame(root, port, id)
          root.protocol("WM_DELETE_WINDOW", root.destroy)
          root.mainloop()              
          print("student left the class")
          sys.exit(0)
          break;
      
          # client_socket.send(bytes(id, "utf8"))
          
                  
      # 선생님 로그인 case
      elif mode == "T":              
        root = Tk()
        root.resizable(False, False)
        root.geometry("765x580+100+100")                    
        
        port = 0
        vport = 0
        if id=="javascript":
          port = 4000
          
          # 통화서버
          vport = 50007
          Thread(target=vserver.main, args=(vport,)).start()
        elif id =="python":          
          port = 5000
          
          # 통화서버
          vport = 50008
          Thread(target=vserver.main, args=(vport,)).start()

        app = editorT.MyFrame(root, port, id, address)                    
        root.mainloop()        
        print("tutor left the class")    
        sys.exit(0)    
        break;

      # 로그인 실패 case
      else :
        print("로그인이 실패하여 프로그램을 종료합니다. 다시 시작해 주세요.")
        client_socket.send(bytes("error", "utf8"))
        quit()  
      
    except OSError: 
      break

HOST = '127.0.0.1'
PORT = 33000

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# 연결되는 애의 address를 넣어줘야함
address = client_socket.recv(BUFSIZ).decode("utf8") 

id = input("Insert id : ")
pw = getpass("Insert pw : ")

client_socket.send(bytes(id, "utf8"))
client_socket.send(bytes(pw, "utf8"))

receive_thread = Thread(target=receive, args=(address,))
receive_thread.start()