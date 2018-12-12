from socket import *
import threading
import time
import sys

global whole_message


whole_message = []


def print_normal():
    for _ in range(5):
        if len(whole_message) > 0:
            print(whole_message[0])
            del whole_message[0]
            break
        time.sleep(2)


def flush_received():
    for message in whole_message:
        if message[:2] == "g_":
            print(message[2:])
            whole_message.remove(message)


def thread_start(client_socket):
    t1 = threading.Thread(target=receive_loop, args=[client_socket])
    t1.start()


def receive_loop(client_socket):
    while True:
        received_message = client_socket.recv(10240).decode()
        if len(received_message) > 0:
            whole_message.append(received_message)


def register_file(client_socket):
    register_file_name = input("Which file to register? : ")
    client_socket.send(register_file_name.encode())


def get_file_download(client_socket):
    get_file_name = input("which file to download? : ")

    client_socket.send(get_file_name.encode())
    time.sleep(5)
    flush_received()
    temp_list = get_file_name.split('/')
    received_file_data = whole_message[0]
    with open(temp_list[len(temp_list)-1], 'w') as f:
        f.write(received_file_data)
    del whole_message[0]
    time.sleep(3)
    flush_received()

    print_normal()


def run_main_client(client_socket):
    thread_start(client_socket)
    time.sleep(5)
    flush_received()
    for message in whole_message:
        print(message)
        whole_message.remove(message)

    while True:
        request_type = input('Enter your word : ')
        if request_type == "0":
            client_socket.send(request_type.encode())
            flush_received()
            time.sleep(5)
            print_normal()

        elif request_type == "1":
            client_socket.send(request_type.encode())
            register_file(client_socket)
            time.sleep(5)

        elif request_type == "2":
            client_socket.send(request_type.encode())
            time.sleep(5)
            flush_received()
            print_normal()

        elif request_type == "3":
            client_socket.send(request_type.encode())
            get_file_download(client_socket)
            time.sleep(3)

        else:
            client_socket.send(request_type.encode())
            print_normal()
            break

        flush_received()

    sys.exit()

def request_socket():
    server_port = 10080
    user_id = input("Enter UserID: ")
    request_ip = input("Enter Relay ServerIP: ")

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((request_ip, server_port))
    client_socket.send(user_id.encode())

    run_main_client(client_socket)


if __name__ == "__main__":
    request_socket()
else:
    print("NOT MODULE USAGE")

