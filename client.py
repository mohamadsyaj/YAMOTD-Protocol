import socket
import sys
from sqlite3 import connect

# make sure the port number match the server
PORT = 16948

# main client logic
def start_client(server_ip):
    # creating a TCP socket
    s = socket.socket()

    # connect to the server IP and the initialized port number
    s.connect((server_ip, PORT))

    # main while loop to for the user to display the commands and send them to the server
    while True:
        cmd = input("Type command (MSGGET, MSGSTORE, QUIT, SHUTDOWN): ").strip().upper()

        # send commands to the server
        s.send((cmd + '\n').encode())

        # reading the response from the server and displaying it to the user
        reply = s.recv(1024).decode().strip()
        print("Server:", reply)

        # to handle the change of the message after changing it
        # and send the new one to the server
        if cmd == "MSGSTORE" and reply == "200 OK":
            message = input("Type new MOTD: ")
            s.send((message + '\n').encode())
            confirm = s.recv(1024).decode().strip()
            print("Server:", confirm)

        # to handle when the user want to shut down
        # and send the password to the server to check
        elif cmd == "SHUTDOWN" and reply == "300 PASSWORD REQUIRED":
            pwd = input("Enter password: ")
            s.send((pwd + '\n').encode())
            reply2 = s.recv(1024).decode().strip()
            print("Server:", reply2)
            if reply2 == "200 OKAY":
                break
        # disconnect client after request
        elif cmd == "QUIT":
            break
    # end socket connection after finished
    s.close()
    print("Disconnected from server.")

# check if the user is provided with the IP address before connection
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <server_ip>")
    else:
        start_client(sys.argv[1])
