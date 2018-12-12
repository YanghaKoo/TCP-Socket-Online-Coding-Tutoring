import os
import sys
from socket import AF_INET, socket, SOCK_STREAM
from tkinter import *
from tkinter.ttk import *
from threading import Thread

class MyFrame(Frame):
    def __init__(self, master, port, id, address):
      s = socket(AF_INET, SOCK_STREAM)
      a = socket(AF_INET, SOCK_STREAM)

      self.HOST = address 

      Frame.__init__(self, master)

      self.port = port
      self.master = master
      self.master.title(f"Tutor side - {id}")
      self.pack(fill=BOTH, expand=True)
      frame3 = Frame(self)
      frame3.pack(fill=BOTH)

      notebook=Notebook(width=300, height=300)
      notebook.pack()

      # editor 영역
      txtComment = Text(frame3) 
      
                   
      def keyPressed(event):      
        try :         
          a.sendall(txtComment.get("1.0",'end-1c').encode())
        except WindowsError as e:
          pass        
      
      txtComment.bind('<Key>', keyPressed)   
      txtComment.pack(fill=X, pady=10, padx=10)
      
      # Execute result
      frame2 = Frame(self)
      frame2.pack(fill=X)

      lblComp = Label(frame2, text="Execute Result", width=20)
      lblComp.pack(side=LEFT, padx=10, pady=10)

      entryComp = Text(frame2, height=10, width=120)
      entryComp.pack(side=RIGHT, padx=10, pady=10)
      entryComp.insert(END, 'waiting for connection...')

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
          #print(line)            
          while line: 
              entryComp.insert(END,line + '\n')               
              #print(line)
              line = f.readline().strip()

      def rcv(s):                
        s.bind(('',port)) 
        s.listen(1) 
        conn, addr = s.accept()
                   
        while True:            
          try :
            data = conn.recv(1024)    
            decoded = data.decode()         

            if decoded=='USEIF3GolLWkJtCH75HW':              
              try:
                a.connect((self.HOST, port + 1))   
              except WindowsError as e:
                self.HOST = '192.168.43.195'
                a.connect((self.HOST, port + 1))   
              
              entryComp.delete('1.0',END)
              entryComp.insert(END, 'Connected with Student!')
            else :
              txtComment.delete(1.0,END)
              txtComment.insert(END,decoded)                                    
          except WindowsError as e:
            pass        

      # execute 버튼 클릭
      btnSave.bind('<Button-1>', execPython)
      btnSave.pack(side=RIGHT, padx=10, pady=10)

      btn2.bind('<Button-1>', execJS)
      btn2.pack(side=RIGHT, padx=10, pady=10)
      
      p = Thread(target=rcv, args=(s,))
      p.start()


if __name__ == '__main__':
      root = Tk()
      root.resizable(False, False)
      root.geometry("765x580+100+100")
      
      app = MyFrame(root, 4000, "idsample", '127.0.0.1')    
      root.mainloop()
      quit()


