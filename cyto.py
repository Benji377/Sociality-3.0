from tkinter import *
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os.path
import webbrowser
import tkinter.ttk as ttk
import tkinter.scrolledtext as ScrolledText
import time


def helping_button():
    webbrowser.open("https://www.internetking.ga/2020/06/sociality-gets-update-sociality-30.html")


class TkinterGUIExample(Tk):

    def __init__(self, *args, **kwargs):

        """
        Create & set window variables.
        """

        Tk.__init__(self, *args, **kwargs)
        self.chatbot = ChatBot(
            "Cyto Bot",
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch'
                },
                {
                    'import_path': 'chatterbot.logic.MathematicalEvaluation'
                }
            ],
            database_uri="sqlite:///database.sqlite3"
        )
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        trainer.train('chatterbot.corpus.english')

        self.title("Sociality 3.0 - CytoBot")

        self.resizable(0, 0)
        self.wm_iconbitmap('favicon.ico')
        
        self.initialize()

    def initialize(self):
        """
        Set window layout.
        """
        self.grid()

        self.style = ttk.Style()
        self.style.configure("Blue.TLabel", foreground="deepskyblue")
        self.style.configure("Red.TButton", font=("arial", 15, "bold"), foreground="red")
        self.style.configure("Green.TButton", font=("arial", 10, "bold"), foreground="green")
        self.style.configure("Top.TLabel", font=("arial", 20, "bold"), foreground="steelblue")

        self.toptitle = ttk.Label(self, anchor=E, text="Sociality", style="Top.TLabel")
        self.toptitle.grid(column=0, row=0, sticky='nesw', padx=3, pady=3)

        self.respond = ttk.Button(self, text='Get Response', command=self.get_response, style="Red.TButton")
        self.respond.grid(column=1, row=1, sticky='nesw', padx=3, pady=3)

        self.usr_input = ttk.Entry(self, state='normal')
        self.usr_input.grid(column=0, row=1, sticky='nesw', padx=3, pady=3)

        self.conversation = ScrolledText.ScrolledText(self, state='disabled')
        self.conversation.grid(column=0, row=2, columnspan=2, sticky='nesw', padx=3, pady=3)

        self.credits = ttk.Label(self, text="Created by Benjamin Demetz", style="Blue.TLabel")
        self.credits.grid(column=0, row=3, sticky='nesw', padx=3, pady=3)

        self.help_button = ttk.Button(self, text='Click here for help', command=helping_button, style="Green.TButton")
        self.help_button.grid(column=1, row=3, sticky='nesw', padx=3, pady=3)

    def get_response(self):
        """
        Get a response from the chatbot and display it.
        """
        user_input = self.usr_input.get()
        self.usr_input.delete(0, END)

        response = self.chatbot.get_response(user_input)

        self.conversation['state'] = 'normal'
        self.conversation.insert(
            END, "Human: " + user_input + "\n" + "CytoBot: " + str(response.text) + "\n"
        )
        self.conversation['state'] = 'disabled'

        time.sleep(0.5)


gui_example = TkinterGUIExample()
gui_example.mainloop()
time.sleep(1)
os.remove("database.sqlite3")
