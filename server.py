import socket
from threading import Thread

TCP_IP="127.0.0.1"
T_PORT=5006
BUF_SIZE=30

clients=[]

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((TCP_IP,T_PORT))
s.listen(1)
print(f"Listening on {TCP_IP}:{T_PORT}")

def client_msg(client,index):
    while True:
        try:
            data=client[0].recv(BUF_SIZE)
        except Exception as e:
            print("Error with client at "+str(client[1])+" "+str(e))
        print("Message recieved: "+str(data.decode()))
        for i in range(len(clients)):
            #if(i!=index):
            clients[i][0].send(data)
while True:
    con,addr=s.accept()
    clients.append([con,addr])
    index=len(clients)-1
    name=con.recv(BUF_SIZE).decode()
    con_msg="New client connected at "+str(addr)+" Name: "+str(name)
    print(con_msg)
    t=Thread(target=client_msg,args=[[con,addr],index])
    t.start()
for i in clients:
    i[0].send("Connection Ended".encode())
    i[0].close()
con.close()
