import socket
import threading
from datetime import datetime
import os
from tkinter import *
from tkinter import messagebox as MessageBox
import time
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
dtn = datetime.now()
FILE_NAME_LOG = f"appservidor/Logs/"+str(dtn.year)+"-"+str(dtn.month)+"-"+str(dtn.day)+"-"+str(dtn.hour)+"-"+str(dtn.minute)+"-"+str(dtn.second)+"-log.txt"
creacion = dtn.microsecond  
resultado = MessageBox.askokcancel("Salir", 
"¿Acepta usar el archivo de 100MB? De lo contrario, se usará el de 250MB para la prueba.")
if resultado == True:
    filename = "appservidor/files/100MB.txt"
else: 
    filename = "appservidor/files/250MB.txt"

def handle_client(conn, addr):
    numeroClientes = ""
    print(f"\n[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT) 
        if msg == DISCONNECT_MSG:
            connected = False
        
        print(f"\n[{addr}] {msg}")
        if msg.isnumeric():
            connections[int(msg)]=conn
        
        if msg[0]=='R':
            print("\ninicia start")
            numeroClientes = msg
            barrier.wait()
            print("\nwait released")
            file = open(filename, 'rb')
            msg = file.read()
            conn.send(msg)  
            fileLog = open(FILE_NAME_LOG, 'ab')
            minutoCreacion = int(FILE_NAME_LOG.split("-")[4])
            segundoCreacion = int(FILE_NAME_LOG.split("-")[5])
            newDtn = datetime.now()
            minutoActual = newDtn.minute
            segundoActual = newDtn.second
            microSegundoActual = newDtn.microsecond
            diferenciaMinuto = minutoActual-minutoCreacion
            diferenciaSegundo = segundoActual-segundoCreacion
            msgLog = "Nombre archivo enviado: "+filename.split("/")[2]+ "\n Tamaño archivo: " +str(os.path.getsize(filename)) +"\n Cliente: " + numeroClientes + "\n Entrega: exitosa" + "\n Tiempo estimado: "+str(diferenciaMinuto)+" minutos, "+str(diferenciaSegundo)+" segundos y "+str(microSegundoActual)+" microsegundos."
            fileLog.write(str.encode("\n"+msgLog))
            fileLog.close()
            connected = False   
        else:
            print(f"\nmsg0!=r")   
            msg = f"Msg received: {msg}"
            conn.send(msg.encode(FORMAT))
        
        
    conn.close()



def main():
    
    for i in range(TOTAL_CONNECTIONS):
        connections.append(0)
        
    print("\n[STARTING] server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"\n[LISTENING] server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount()-1}")



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