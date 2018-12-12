from socket import *
import time
import threading

global message_box
global notice_box
global global_file_list
global user_list
global t_lock

t_lock = threading.Lock()

global_file_list = ['Readme.md']

user_list = []

message_box = '''
0
########################
1. Register a file
2. Get the global file list
3. Download a file
4. Exit
########################
'''
notice_box = {
        "g_welcome": "g_[Notice]Welcome ",
        "g_update": "g_[Notice]Global file list is updated",
        "g_left": "g_[Notice]Left client : "
        }


def main_server(connection_socket):
    user_id = connection_socket.recv(1024).decode()
    print(user_id+" entered")
    for every_client in user_list:
        every_client.send((notice_box["g_welcome"] + user_id).encode())

    connection_socket.send(message_box.encode())
    while True:
        user_request_type = connection_socket.recv(1024).decode()

        if user_request_type == "0":
            connection_socket.send(message_box.encode())

        elif user_request_type == "1":
            user_registered_filename = connection_socket.recv(1024).decode()
            global_file_list.append(str(user_id + "/" + user_registered_filename))
            print(user_id, "registered", user_registered_filename, "\n", global_file_list)
            for every_client in user_list:
                every_client.send(notice_box["g_update"].encode())

        elif user_request_type == "2":
            send_list = "The global file list is as follows:"
            for global_file in global_file_list:
                send_list += "\n" + global_file
            connection_socket.send(send_list.encode())

        elif user_request_type == "3":
            user_request_filename = connection_socket.recv(1024).decode()
            with open(user_request_filename, 'rb') as f:
                file_content = f.read()
            connection_socket.sendall(file_content)
            time.sleep(1)
            connection_socket.send("Download completed".encode())

            temp_list = user_request_filename.split('/')
            global_file_list.append(str(user_id + "/" + temp_list[len(temp_list) - 1]))
            time.sleep(1)
            for every_client in user_list:
                every_client.send(notice_box["g_update"].encode())

        elif user_request_type == "4":
            connection_socket.send("Notified RelayServer\nGoodbye!".encode())
            connection_socket.close()
            user_list.remove(connection_socket)
            print(user_id + " exit")
            for every_client in user_list:
                every_client.send((notice_box["g_left"] + user_id).encode())
            break

        else:
            break


def run_socket():
    server_port = 10080
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(10)
    print('The TCP server is ready to receive')
    while True:
        connection_socket, address = server_socket.accept()
        user_list.append(connection_socket)
        t1 = threading.Thread(target=main_server, args=[connection_socket])
        t1.start()


if __name__ == "__main__":
    run_socket()
else:
    print("NOT MODULE USAGE")