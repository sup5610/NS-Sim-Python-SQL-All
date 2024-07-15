
# INTEGRATE THIS TO THE USER WINDOW IN THE LOG IN SYSTEM

import tkinter as tk, socket, json, time, math
from tkinter import ttk
socket.setdefaulttimeout(1)

# original functions
# def InitThread():
#     host, port = "127.0.0.1", 64738
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((host, port))
#     return sock
    
# def SendInfo(data):
#     sock = InitThread()
#     sent = False
#     while True:
#         while (not sent):
#             try:
#                 print("sending")
#                 sock.sendall(data.encode("UTF-8"))
#                 received = sock.recv(1024).decode("UTF-8")
#             except:
#                 received = False
#                 print("socket currently closed")
                
#             time.sleep(0.2)
#             if (received == "success"):
#                 sent = True
#                 print("success")

host, port = "127.0.0.1", 64738
global sock
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((host, port))
except:
    print("Connection not open on from Unity")




# SendInfo("Testing Testing")
# SendInfo("instwolf")


class app():
    def __init__(self, master):
        self.root = master
        master.lift()
        master.geometry("600x600")


        self.e1 = tk.Entry(master)
        self.e1.pack()
        self.b1 = tk.Button(master)
        self.b1.config(text = "Send data", command = lambda : self.SendInfo(self.e1.get()))
        self.b1.pack()


        self.wolvesLabel = tk.Label(master, text = "{Spawn wolves}: 0")
        self.wolvesLabel.pack()
        self.deerLabel = tk.Label(master, text = "{Spawn deer}: 0")
        self.deerLabel.pack()
        self.rabbitsLabel = tk.Label(master, text = "{Spawn rabbits}: 0")
        self.rabbitsLabel.pack()
        self.jaguarsLabel = tk.Label(master, text = "{Spawn jaguars}: 0")
        self.jaguarsLabel.pack()

        self.wolvesScale = ttk.Scale(master, name = "wolvesScale", from_ = 0, to = 10, orient = "horizontal", command = self.WolvesEvent)
        self.wolvesScale.pack()
        self.deerScale = ttk.Scale(master, name = "deerScale", from_ = 0, to = 10, orient = "horizontal", command = self.DeerEvent)
        self.deerScale.pack()
        self.rabbitsScale = ttk.Scale(master, name = "rabbitsScale", from_ = 0, to = 10, orient = "horizontal", command = self.RabbitsEvent)
        self.rabbitsScale.pack()
        self.jaguarsScale = ttk.Scale(master, name = "jaguarsScale", from_ = 0, to = 10, orient = "horizontal", command = self.JaguarsEvent)
        self.jaguarsScale.pack()

        self.spawnButton = tk.Button(master)
        self.spawnButton.config(text = "spawn from slider", command = lambda : self.Spawn())
        self.spawnButton.pack()

    def WolvesEvent(self, value):
        rounded = round(float(value))
        self.wolvesLabel["text"] = "Spawn wolves:", rounded
    def DeerEvent(self, value):
        rounded = round(float(value))
        self.deerLabel["text"] = "Spawn deer:", rounded
    def RabbitsEvent(self, value):
        rounded = round(float(value))
        self.rabbitsLabel["text"] = "Spawn rabbits:", rounded
    def JaguarsEvent(self, value):
        rounded = round(float(value))
        self.jaguarsLabel["text"] = "Spawn jagurs:", rounded

        

    def SendInfo(self, data):
        sent = False
        attempts = 0
        if data == "" or data == None:
            print("Invalid")
        else:
            while (not sent and attempts < 10):
                try:
                    print("sending")
                    sock.sendall(data.encode("UTF-8"))
                    received = sock.recv(1024).decode("UTF-8")
                except:
                    received = False
                    attempts += 1
                    print("socket currently closed")
                    
                time.sleep(0.2)
                if (received == "success"):
                    sent = True
                    print("success")


    def Spawn(self):
        spawnNumbers = {
        "wolf": round(self.wolvesScale.get()),
        "deer": round(self.deerScale.get()),
        "rabbit": round(self.rabbitsScale.get()),
        "jaguar": round(self.jaguarsScale.get())
        }
        
        for i in spawnNumbers.keys():
            for j in range(spawnNumbers[i]):
                self.SendInfo("inst"+i)
                # print("inst"+i)
                # self.SendInfo("inst"+str(spawnNumbers[i]))







        # for i in spawnNumbers.keys():
        #     print(i)
        #     print(spawnNumbers[i])



# def SendInfo(data):
#     sock = InitThread()
#     sent = False
#     print("sending")on
#     if (sock.sendall(data.encode("UTF-8")) == None): # is data sent, return is 0, else raise error. However sent does not mean received
#         print("sent")
#     received = sock.recv(1024).decode("UTF-8")

# SendInfo("Test")

root = tk.Tk()
app(root)


root.mainloop()