import socket
import random
#from threading import Thread
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk


host = "192.168.4.27"
port = 9876
clientSocket = socket.socket()
print(f"Connecting to {host}:{port}...")
# connect to the server
clientSocket.connect((host, port))
print("Success!")
# prompt the client for a name
#name = input("Enter username: ")
#name = name + ": "
#print("Enter message (quit() to exit): ")
#def recvMsg():
    #while True:
        #message = clientSocket.recv(1024).decode('utf-8')
        #print("\n" + message)
#recvThread = Thread(target=recvMsg) # thread for recieving messages
#recvThread.daemon = True
#recvThread.start()
#while True:
    #msgSend =  input() # need input to send next message to server
    #if msgSend == 'quit()':
       # break
    #clientSocket.send(name.encode('utf-8') + msgSend.encode('utf-8'))
#clientSocket.close() # close client socket


#Class for Graphical User Interface
class GUI():
    def __init__(self): #Constructor method

        self.Window = Tk()
        self.Window.withdraw()


        #Login Window
        self.login = Toplevel()
        self.login.title("Login")
        self.login.configure(width = 400, height = 300)
        self.login.resizable(width = False, height = False)

        self.pls = Label(self.login, text = "Login to continue", justify = CENTER, font = "Arial 15 bold")
        self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.07)

        self.labelName = Label(self.login, text = "Name", font = "Arial 12")
        self.labelName.place(relheight = 0.2, relx = 0.1, rely = 0.2)

        #Entry box for typing messages
        self.entryName = Entry(self.login, font = "Arial 15")
        self.entryName.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.2)


        #Curser Focus
        self.entryName.focus()

        #Continue Button
        self.go = Button(self.login, text = "Continue", font = "Arial 12 bold", command = lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx = 0.4, rely = 0.55)
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        #Recieve Messages
        recv = threading.Thread(target = self.recieve)
        recv.start()

    #Main Layout
    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("ChatApp")
        self.Window.configure(width = 470, height = 550, bg = "#17202A")
        self.Window.resizable(width = False, height = False)
        self.labelHead = Label(self.Window, text = self.name, font = "Arial 11 bold", bg = "#17202A", fg = "#EAECEE", pady = 5)
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window, width = 450, bg = "#ABB2B9")
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)
        self.textCons = Text(self.Window, width = 20, height = 2, bg = "#17202A", fg = "#EAECEE", font = "Arial 12", padx = 5, pady = 5)
        self.textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08)
        self.labelBottom = Label(self.Window, bg = "#ABB2B9", height = 80)
        self.labelBottom.place(relwidth = 1, rely = 0.825)
        self.entryMsg = Entry(self.labelBottom, bg = "#2C3E50", fg = "#EAECEE", font = "Arial 12")
        self.entryMsg.place(relwidth = 0.74, relheight = 0.06, rely = 0.008, relx = 0.011)

        self.entryMsg.focus()

        #Send Button
        self.buttonSend = Button(self.labelBottom, text = "Send", font = "Arial 10 bold", width = 20, bg = "#ABB2B9", command = lambda : self.sendButton(self.entryMsg.get()))
        self.buttonSend.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22)

        self.textCons.config(cursor = "arrow")

        #Scroll bar
        scrollBar = Scrollbar(self.textCons)
        scrollBar.place(relheight = 1, relx = 0.974)
        scrollBar.config(command = self.textCons.yview)
        self.textCons.config(state = DISABLED)
    
    #Start sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target = self.sendMessage)
        snd.start()

    #Recieve Messages
    def recieve(self):
        while True:
            try: 
                message = clientSocket.recv(1024).decode('utf-8')
                if message == 'NAME':
                    clientSocket.send(self.name.encode('utf-8'))
                else:
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END, message + "\n\n")
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
            except:
                print("Error has occred!")
                clientSocket.close()
                break
    
    #Sending Messages
    def sendMessage(self):
        self.textCons.config(state = DISABLED)
        while True:
            if self.msg == 'quit()':
                message = (f"{self.name} Disconnected...")
                clientSocket.send(message.encode('utf-8'))
                clientSocket.close()
                break
            else:
                message = (f"{self.name}: {self.msg}")
                clientSocket.send(message.encode('utf-8'))
                break



g = GUI()


        

