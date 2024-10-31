import socket
from threading import Thread
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import tkinter.colorchooser as colorchooser

TCP_IP="127.0.0.1"
T_PORT=5006
BUF_SIZE=1024

#MAIN_BG_COLOR="#cecece"
#MAIN_FONT_COLOR="#000000"
#SERVER_MSG_FONT_COLOR="#515151"
MAIN_BG_COLOR="#1c1b1b"
MAIN_FONT_COLOR="#cecece"
SECONDARY_BG_COLOR="#333131"
SERVER_MSG_FONT_COLOR="#a8a8a8"

window=None
msg_text=None
inputtext=None
sendbtn=None
settings_btn=None

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
def settings_win():
    pop=tk.Toplevel()
    pop.geometry("230x155")
    pop.configure(bg=MAIN_BG_COLOR)
    pop.resizable(width=False,height=False)
    #Increase with each button
    itemnum=0
    closebtn=tk.Button(pop,text="Close",command=pop.destroy) 
    closebtn.configure(foreground=MAIN_FONT_COLOR,bg=SECONDARY_BG_COLOR,activebackground=MAIN_BG_COLOR,activeforeground=MAIN_FONT_COLOR)
    closebtn.grid(column=0,row=itemnum+1)


window.geometry("500x500")
window.resizable(width=False,height=False)
window.protocol("WM_DELETE_WINDOW",close)
window.configure(bg=MAIN_BG_COLOR)
inputtext=tk.Entry(width=50)
inputtext.grid(column=0,row=2)
inputtext.bind("<Return>",send_reroute)
inputtext.configure(foreground=MAIN_FONT_COLOR,bg=SECONDARY_BG_COLOR,insertbackground=MAIN_FONT_COLOR)
inputtext.focus()
sendbtn=tk.Button(width=5,text="Send",command=lambda: send(inputtext))
sendbtn.grid(column=1,row=2)
sendbtn.configure(foreground=MAIN_FONT_COLOR,bg=SECONDARY_BG_COLOR,activebackground=MAIN_BG_COLOR,activeforeground=MAIN_FONT_COLOR)
msg_text=scrolledtext.ScrolledText(width=60,height=25)
msg_text.grid(column=0,row=1,columnspan=2)
msg_text.configure(state="disabled", foreground=MAIN_FONT_COLOR, bg=SECONDARY_BG_COLOR)
msg_text.vbar.configure(troughcolor=MAIN_BG_COLOR,bg=SECONDARY_BG_COLOR)
settings_btn=tk.Button(text="Settings",command=lambda:settings_win())
settings_btn.grid(row=0,column=1)
settings_btn.configure(foreground=MAIN_FONT_COLOR,bg=SECONDARY_BG_COLOR,activebackground=MAIN_BG_COLOR,activeforeground=MAIN_FONT_COLOR)


s.send(name.encode())
def listen():
    while True:
        dmsg=s.recv(BUF_SIZE)
        msg_text.configure(state="normal")
        msg_text.insert(tk.END,dmsg.decode()+"\n")
        if(not(":" in dmsg.decode())):
            msg_text.tag_add("server","end-2c linestart","end-2c")
        msg_text.tag_configure("server",foreground=SERVER_MSG_FONT_COLOR)
        msg_text.configure(state="disabled")
        msg_text.yview(tk.END)
t=Thread(target=listen)
t.daemon=True
t.start()
window.mainloop()
s.close()
