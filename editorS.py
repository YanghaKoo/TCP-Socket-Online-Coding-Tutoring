import os
import sys
from socket import AF_INET, socket, SOCK_STREAM
from tkinter import *
from tkinter.ttk import *
from threading import Thread
  

class MyFrame(Frame):
    def __init__(self, master, port, id):        
        s = socket(AF_INET, SOCK_STREAM)

        HOST = '127.0.0.1' 

        s.connect((HOST, port))   # port   
        Frame.__init__(self, master)

        self.master = master
        self.master.title(f"Student side - {id}")
        self.pack(fill=BOTH, expand=True)
        frame3 = Frame(self)
        frame3.pack(fill=BOTH)

        notebook=Notebook(width=300, height=300)
        notebook.pack()
        
        # code editor 영역
        txtComment = Text(frame3)
        def keyPressed(event):                              
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
        entryComp.insert(END, 'Connected with Tutor!')
 
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
            while line: 
                entryComp.insert(END,line + '\n')                              
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
            while line: 
                entryComp.insert(END,line + '\n')               
                #print(line)
                line = f.readline().strip()
        
        
        # wait
        def rcv(s):          
          with socket(AF_INET, SOCK_STREAM) as a:
            a.bind(('',port+1)) # port + 1
            a.listen(1) #4001에서 listen

            s.sendall('USEIF3GolLWkJtCH75HW'.encode()) 

            conn2, addr2 = a.accept()                                 
            while True:            
              data = conn2.recv(1024)  
              decoded = data.decode()

              txtComment.delete(1.0,END)
              txtComment.insert(END,decoded)  

        # compile 버튼 클릭
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
  
  app = MyFrame(root, 4000, "idsample")
  root.mainloop()
  quit()
