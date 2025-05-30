import socket
import threading

# setting the port number for the server to listen on
PORT = 16948

# default message of the day
motd = "An apple a day keeps the doctor away."

# password to shut down the server
password = "123?abc"

# lock to protect threads when changing the message
lock = threading.Lock()

# shared flag to control server running state
server_running = True
server_socket = None  # reference to main socket

# function to handle the communication with one client
def handle_client(conn, addr):
    global motd, server_running, server_socket
    print(f"Connected by {addr}")
    waiting_msg = False

    try:
        while True:
            # Receive data from user and break if no data found
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            print(f"Client {addr}: {data}")
            # waiting for the message from the user and update the global message
            if waiting_msg:
                with lock:
                    motd = data
                conn.send(b"200 OK\n")
                waiting_msg = False
                continue
            # to handle all the user different commands
            if data == "MSGGET":
                with lock:
                    msg = motd
                conn.send(f"200 OK\n{msg}\n".encode())

            elif data == "MSGSTORE":
                conn.send(b"200 OK\n")
                waiting_msg = True

            elif data == "QUIT":
                conn.send(b"200 OK\n")
                break

            elif data == "SHUTDOWN":
                conn.send(b"300 PASSWORD REQUIRED\n")
                pwd = conn.recv(1024).decode().strip()
                if pwd == password:
                    conn.send(b"200 OKAY\n")
                    server_running = False  # set server stop flag
                    server_socket.close()   # close main server socket

                    # dummy connection to unblock accept()
                    try:
                        dummy = socket.socket()
                        dummy.connect(("127.0.0.1", PORT))
                        dummy.close()
                    except:
                        pass

                    break
                else:
                    conn.send(b"301 WRONG PASSWORD\n")
            # default statement in case any unrecognized command
            else:
                conn.send(b"400 UNKNOWN COMMAND\n")

    except Exception as e:
        print(f"[ERROR with {addr}] {e}")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")

# turn on the server and accept new connections
def start_server():
    global server_running, server_socket
    # create TCP socket
    s = socket.socket()
    server_socket = s  # assign socket reference for shutdown
    # Let the server accept connections on any IP address on computer
    s.bind(('', PORT))
    # max 2 clients connect
    s.listen(2)
    print(f"Server listening on port {PORT}")

    try:
        while server_running:
            try:
                # Accept a new client connection
                conn, addr = s.accept()
                # Start a new thread to handle the client
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
            except OSError:
                break  # socket closed by SHUTDOWN
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        s.close()
        print("Server fully shut down.")

# run the server
start_server()
