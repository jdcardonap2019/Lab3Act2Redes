import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
TOTAL_CONNECTIONS = 25
connections = []
requiredCons = 10
barrier = threading.Barrier(requiredCons) 


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT) 
        if msg == DISCONNECT_MSG:
            connected = False
        
        print(f"[{addr}] {msg}")
        if msg.isnumeric():
            connections[int(msg)]=conn
        
        if msg[0]=='R':
            print("inicia start")
            barrier.wait()
            print("wait released")
            filename = "files/test1.txt"
            file = open(filename, 'rb')
            msg = file.read(SIZE)
            conn.send(msg)
            connected = False   
        else:
            print(f"msg0!=r")
            msg = f"Msg received: {msg}"
            conn.send(msg.encode(FORMAT))
        
        
    conn.close()



def main():
    
    for i in range(TOTAL_CONNECTIONS):
        connections.append(0)
        
    print("[STARTING] server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")



main()


"""
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_addresses = []

def create_socket():
    try: 
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as mag:
        print("Socket creation error: "+str(mag))

def bind_socket():
    try:
        global host
        global port
        global s

        s.bind((host, port))
        s.listen(25)
    except socket.error as mag:
        print("Socket binding error: "+str(mag))
        bind_socket()

def socket_accept():
    conn, address = s.accept()
    
    conn.close()


s = socket.socket()
host = socket.gethostname()
port = 8080
s.bind((host,port))
s.listen(25)
print(host) 
print("Waiting for connections")
conn, addr = s.accept()
print(addr, "Has connected to the server")

"""