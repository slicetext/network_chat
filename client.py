import socket
from threading import Thread
import tkinter as tk
import tkinter.scrolledtext as scrolledtext

TCP_IP="127.0.0.1"
T_PORT=5006
BUF_SIZE=1024

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((TCP_IP,T_PORT))

name=input("What's your name?: ")
window=tk.Tk()
def close():
    window.destroy()
    s.close()
    exit()
def send(entry):
    msg=name+": "+entry.get()
    s.send(msg.encode())
    entry.delete(0,"end")
def send_reroute(e):
    send(e.widget)
window.geometry("500x500")
window.resizable(width=False,height=False)
window.protocol("WM_DELETE_WINDOW",close)
inputtext=tk.Entry(width=50)
inputtext.grid(column=0,row=0)
inputtext.bind("<Return>",send_reroute)
inputtext.focus()
sendbtn=tk.Button(width=5,text="Send",command=lambda: send(inputtext)).grid(column=1,row=0)
msg_text=scrolledtext.ScrolledText(width=60,height=27)
msg_text.grid(column=0,row=1,columnspan=2)
msg_text.configure(state="disabled")


s.send(name.encode())
def listen():
    while True:
        dmsg=s.recv(BUF_SIZE)
        msg_text.configure(state="normal")
        msg_text.insert(tk.END,dmsg.decode()+"\n")
        msg_text.configure(state="disabled")
        msg_text.yview(tk.END)
t=Thread(target=listen)
t.daemon=True
t.start()
window.mainloop()
s.close()
