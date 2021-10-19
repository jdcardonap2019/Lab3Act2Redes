import tkinter as tk
from tkinter import filedialog, Text
import os
from datetime import datetime
import socket 
import threading
from pathlib import Path
from functools import partial

IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
TOTAL_CONNECTIONS = 25
dtn = datetime.now()
FILE_NAME_LOG = f"Logs/"+str(dtn.year)+"-"+str(dtn.month)+"-"+str(dtn.day)+"-"+str(dtn.hour)+"-"+str(dtn.minute)+"-"+str(dtn.second)+"-log.txt"

connected_clients = []
client_buttons = []
clientes = []
client_active = []


"""
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server {IP}:{PORT}")

    connected = True
    while connected:
        msg = input("> ")
        
        client.send(msg.encode(FORMAT))
        
        if msg == DISCONNECT_MSG:
            connected = False
        else: 
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")
"""
def main():
    for x in range(TOTAL_CONNECTIONS):
        connected_clients.append(0)
        client_buttons.append(0)
        clientes.append(0)
        client_active.append(0)
    generateInterface()

def runApp():
    for i in range(TOTAL_CONNECTIONS):
        clientes[i].config(bg="#FF636D")
            
    

def connect_client(clientNum):
    client_active[clientNum]=1
    clientes[clientNum].config(bg="#90FF61")
    connected_clients[clientNum] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected_clients[clientNum].connect(ADDR)
    print(f"\n[CONNECTED] Client {clientNum} connected to server {IP}:{PORT}")
    msg = f"{clientNum}"
    connected_clients[clientNum].send(msg.encode(FORMAT))
    msg = connected_clients[clientNum].recv(SIZE).decode(FORMAT)
    print(f"\n[SERVER->{clientNum}] {msg}")
    task_client(clientNum)

def disconnect_client(clientNum):
    #msg = DISCONNECT_MSG
    #connected_clients[clientNum].send(msg.encode(FORMAT))
    clientes[clientNum].config(bg="#FF636D")
    client_active[clientNum]=0
    

    
    connected_clients[clientNum].close()

def task_client(clientNum):
    try:
        msg = f"R{clientNum}"
        connected_clients[clientNum].send(msg.encode(FORMAT))
        msg = connected_clients[clientNum].recv(SIZE) 
        print("\n maybe")
        filename = f"archivos/Cliente{clientNum}-Prueba-{get_sum_connections()}.txt"
        file = open(filename, 'wb')
        file.write(msg)
        file.close()
        #Creacion Log
        fileLog = open(FILE_NAME_LOG, 'ab')
        '''Con las siguentes lineas el codigo se queda pensando... intentar en otra maquina'''
        #msgLog = "Nombre archivo enviado: "+filename.split("/")[2]+ "\n Tamaño archivo: " +str(os.path.getsize(filename)) +"\n Cliente: " + numeroClientes + "\n Entrega: exitosa" + "\n Tiempo estimado: "+str(diferenciaMinuto)+" minutos, "+str(diferenciaSegundo)+" segundos y "+str(diferenciaMicroSegundo)+" microsegundos."
        #print(msgLog)
        #fileLog.write(str.encode("\n"+msgLog))
        fileLog.write(str.encode("\n Entrega de paquete para cliente: exitosa"))
        fileLog.close()
        print(f"\n[SERVER->{clientNum}] File received!")
    except:
        disconnect_client(clientNum)


    

def select_client(clientNum):
    if(client_active[clientNum]==1):
        disconnect_client(clientNum)
    else:
        thread = threading.Thread(target=connect_client,args=[clientNum])
        thread.start()
        #connect_client(clientNum)
        
def get_sum_connections():
    x = 0
    for i in range(TOTAL_CONNECTIONS):
        if (client_active[i]==1):
            x = x+1
    return x

def connect_all():
    for session in range(TOTAL_CONNECTIONS):
        if (client_active[session]==0):
            thread = threading.Thread(target=connect_client,args=[session])
            thread.start()
    print ("\n[APP] All clients connected")

def connect_five():
    contador = 0
    for session in range(TOTAL_CONNECTIONS):
        if(contador==5):
            break  
        if (client_active[session]==0):
            thread = threading.Thread(target=connect_client,args=[session])
            thread.start()
            contador+=1
        else:
            contador+=1
    print ("\n[APP] Five clients connected")

def connect_ten():
    contador = 0
    for session in range(TOTAL_CONNECTIONS):
        if(contador==10):
            break
        if (client_active[session]==0):
            thread = threading.Thread(target=connect_client,args=[session])
            thread.start()
            contador+=1
        else:
            contador+=1
    print ("\n[APP] Ten clients connected")

def disconnect_all():
    for session in range(TOTAL_CONNECTIONS):
        if (client_active[session]==1):
            disconnect_client(session)
    print ("\n[APP] All clients disconnected")

    



def generateInterface():
    root = tk.Tk()
    canvas = tk.Canvas(root, height=700, width=700, bg="#C1B0E8")
    canvas.pack()

    frame1 = tk.Frame(canvas, bg= "#A193C2")
    frame1.place(relwidth=0.18, relheight=0.8, relx=0.1,rely=0.1)

    frame2 = tk.Frame(canvas, bg= "#A193C2")
    frame2.place(relwidth=0.6, relheight=0.8, relx=0.3,rely=0.1)
    
    generateClients(frame2)

    runAppBt = tk.Button(frame1, text="Run", padx=30,pady=10,fg="#C1B0E8", bg="#4C465C", command=runApp)
    runAppBt.grid(row=1,column=0,padx=5,pady=10)

    connectFiveBt = tk.Button(frame1, text="Connect 5", padx=10,pady=10,fg="#C1B0E8", bg="#4C465C", command=connect_five)
    connectFiveBt.grid(row=2,column=0,padx=5,pady=10)

    connectTenBt = tk.Button(frame1, text="Connect 10", padx=10,pady=10,fg="#C1B0E8", bg="#4C465C", command=connect_ten)
    connectTenBt.grid(row=3,column=0,padx=5,pady=10)

    connectAllBt = tk.Button(frame1, text="Connect All", padx=10,pady=10,fg="#C1B0E8", bg="#4C465C", command=connect_all)
    connectAllBt.grid(row=4,column=0,padx=5,pady=10)

    disconnectAllBt = tk.Button(frame1, text="Disconnect All", padx=10,pady=10,fg="#C1B0E8", bg="#4C465C", command=disconnect_all)
    disconnectAllBt.grid(row=5,column=0,padx=5,pady=10)

    root.mainloop()

def generateClients(frame):
    numCliente = 0
    for i in range(5):
        for j in range(5):
            
            clienteX = tk.Button(frame, text = 'Cliente '+str(numCliente), borderwidth=1, padx=5,pady=25,bg="#FF636D",fg="black",command=partial(select_client,numCliente))
            clienteX.grid(row=i,column=j,pady=15,padx=5)
            clientes[numCliente]=clienteX
            numCliente = numCliente + 1

main()





