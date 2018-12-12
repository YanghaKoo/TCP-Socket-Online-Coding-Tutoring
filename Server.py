from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_incoming_connections():        
    while True:        
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)           
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_address[0],)).start()

def handle_client(client, addr):    
    client.send(bytes(addr, 'utf8')) #주소 보내자        

    id = client.recv(BUFSIZ).decode("utf8")
    pw = client.recv(BUFSIZ).decode("utf8")

    tog = 0
    for name in db:
      if (name == id) and (db[id]['password'] == pw):        
        if db[id]['isLoggedIn'] == False:        
          tog = 1
          db[id]['isLoggedIn'] = True
          print(f'어서오세요 {id}님!')          
          
          # 튜터모드이면 이름만 전달
          if db[id]["mode"] == "T":
            client.send(bytes(id,"utf8"))

          # 학생모드이면 이름 + 로그인한 튜터들 전달
          else :
            arr = []
            for name in db:
              if db[name]['mode'] == "T" and db[name]['isLoggedIn'] == True:
                arr.append(name)

            str = ' '.join(arr)
            print("logged in Tutors : " + str)
            client.send(bytes(id + ' '+ str, "utf8"))
            
        else :
          tog = 1
          print(f'중복 로그인 : {id}')   
          db[id]['isLoggedIn'] = False       
          client.send(bytes('duplicate', 'utf8'))

      
    if tog==0:  
      print('log in failed!')                   
      client.send(bytes('failure', "utf8"))

    #현재 매칭이 되어서 교육중인 선생님은 loggenin을 풀어줌
    try :
      ing = client.recv(BUFSIZ).decode("utf8")
      if ing != "error":
        db[ing]["isLoggedIn"] = False
    except WindowsError as e:
      pass          

clients = {}
addresses = {}

db = {
  "javascript" : {"password" : "1", "mode" : "T", "isLoggedIn" : False},
  "python" : {"password" : "2", "mode" : "T", "isLoggedIn" : False},
  "yangha" : {"password" : "3", "mode" : "S",  "isLoggedIn" : False},
  "koo" : {"password" : "4", "mode" : "S",  "isLoggedIn" : False},    
}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
