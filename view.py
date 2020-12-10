import tkinter
from tkinter import messagebox

CLOSING_PROTOCOL = "WM_DELETE_WINDOW"
END_OF_LINE = "\n"
KEY_RETURN = "<Return>"
TEXT_STATE_DISABLED = "disabled"
TEXT_STATE_NORMAL = "normal"
SEND = "Send"


class DigitLabirintGameUI(object):
    def __init__(self, client):
        self.client = client
        self.operations = list()
        self.gui = None
        self.frame = None
        self.input_field = None
        self.operation = None
        self.message_list = None
        self.scrollbar = None
        self.operation0_button = None
        self.operation1_button = None
        self.operation2_button = None
        self.operation3_button = None
        self.operation4_button = None

    def show(self):
        self.gui = tkinter.Tk()
        self.fill_frame()
        self.gui.protocol(CLOSING_PROTOCOL, self.on_closing)
        # return self.input_dialogs()
        return True

    def loop(self):
        self.gui.mainloop()

    def set_operations(self, operations):
        for i in range(5):
            self.operations[i].set(operations[i])

    def fill_frame(self):
        self.frame = tkinter.Frame(self.gui)
        self.scrollbar = tkinter.Scrollbar(self.frame)
        self.message_list = tkinter.Text(self.frame, state=TEXT_STATE_DISABLED)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        for i in range(5):
            self.operations.append(tkinter.StringVar())  # add to list
            # self.operations[i].set(str(i))
        self.frame.pack()
        self.operation0_button = tkinter.Button(self.gui, textvariable=self.operations[0], command=lambda: self.client.send(0))
        self.operation0_button.pack()
        self.operation1_button = tkinter.Button(self.gui, textvariable=self.operations[1], command=lambda: self.client.send(1))
        self.operation1_button.pack()
        self.operation2_button = tkinter.Button(self.gui, textvariable=self.operations[2], command=lambda: self.client.send(2))
        self.operation2_button.pack()
        self.operation3_button = tkinter.Button(self.gui, textvariable=self.operations[3], command=lambda: self.client.send(3))
        self.operation3_button.pack()
        self.operation4_button = tkinter.Button(self.gui, textvariable=self.operations[4], command=lambda: self.client.send(4))
        self.operation4_button.pack()

    def alert(self, title, message):
        messagebox.showerror(title, message)

    def show_message(self, message):
        self.message_list.configure(state=TEXT_STATE_NORMAL)
        self.message_list.insert(tkinter.END, str(message) + END_OF_LINE)
        self.message_list.configure(state=TEXT_STATE_DISABLED)

    def on_closing(self):
        self.client.exit()
        self.gui.destroy()