import socket
import os
import sys
from tkinter import *
from tkinter.ttk import *
from threading import Thread

def on_closing():
  sys.exi1(1)

class MyFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
 
        self.master = master
        self.master.title("Client side - 201211947 구양하")
        self.pack(fill=BOTH, expand=True)
        frame3 = Frame(self)
        frame3.pack(fill=BOTH)

        notebook=Notebook(width=300, height=300)
        notebook.pack()

        # code editor 영역
        txtComment = Text(frame3)

        
        def keyPressed(event):  
            #print(event.char)                  
            s.sendall(txtComment.get("1.0",'end-1c').encode())

        txtComment.bind('<Key>', keyPressed)         
        txtComment.pack(fill=X, pady=10, padx=10)      
        
        # Execute result
        frame2 = Frame(self)
        frame2.pack(fill=X)
 
        lblComp = Label(frame2, text="Execute Result", width=20)
        lblComp.pack(side=LEFT, padx=10, pady=10)
 
        entryComp = Text(frame2, height=10, width=120)
        entryComp.pack(side=RIGHT, padx=10, pady=10)
 
        # Execute
        frame4 = Frame(self)
        frame4.pack(fill=X)
        btnSave = Button(frame4, text="python")
        
        frame5 = Frame(self)
        frame5.pack(fill=X)
        btn2 = Button(frame5, text="javascript")
        

        # python 실행결과
        def execPython(event):
          content = txtComment.get("1.0",'end-1c')
          entryComp.delete('1.0',END)
          with open('compile.py', 'w') as f:          
            f.write(content)

          os.system('python compile.py > output.txt 2>&1')          
          entryComp.insert(END,"[Below this line are output(std or error) from input code.]\n\n")

          with open('output.txt', 'r') as f:
            line = f.readline().strip()
            print(line)
            # entryComp.insert(END, line)
            while line: 
                entryComp.insert(END,line + '\n')               
                print(line)
                line = f.readline().strip()
            
        # javacsipt 실행결과
        def execJS(event):
          content = txtComment.get("1.0",'end-1c')
          entryComp.delete('1.0',END)
          with open('compile.js', 'w') as f:
            f.write(content)

          os.system('node compile.js > output.txt 2>&1')          
          entryComp.insert(END,"[Below this line are output(std or error) from input code.]\n\n")

          with open('output.txt', 'r') as f:
            line = f.readline().strip()
            print(line)
            # entryComp.insert(END, line)
            while line: 
                entryComp.insert(END,line + '\n')               
                print(line)
                line = f.readline().strip()
        
        
        # 어허 기다려
        def rcv(s):
          print("multi in")
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
            a.bind(('',4001)) # 서버로서의 연결 -> 바인드 (수신
            a.listen(1) #4001에서 listen

            s.sendall('USEIF3GolLWkJtCH75HW'.encode()) # 특정 문자열 전송

            conn2, addr2 = a.accept() # 여기서 멈추는데??
            print(11)                      
            while True:            
              data = conn2.recv(1024)     #여기서 오류            
              decoded = data.decode()

              txtComment.delete(1.0,END)
              txtComment.insert(END,decoded)  

              print(decoded)
              #conn.sendall(data)
              #conn.close()
            print("multi out")                

        # compile 버튼 클릭
        btnSave.bind('<Button-1>', execPython)
        btnSave.pack(side=RIGHT, padx=10, pady=10)

        btn2.bind('<Button-1>', execJS)
        btn2.pack(side=RIGHT, padx=10, pady=10)
        
        p = Thread(target=rcv, args=(s,))
        p.start()
        



# 이거 2줄 다시 살ㄹ려
if __name__ == '__main__':
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect(('127.0.0.1', 4000))       
      
      root = Tk()
      root.resizable(False, False)
      root.geometry("765x580+100+100")
      #root.protocol("WM_DELETE_WINDOW", on_closing)
      
      app = MyFrame(root)
      root.mainloop()
      quit()
