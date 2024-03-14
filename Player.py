"""
This is module Player.py
"""
from tkinter import *


class Player:
    def __init__(self, name, board):
        self.lotherpoint = None
        self.lpoint = None
        self.answer = None
        self.word = None
        self.wordlist = None
        self.entry = None
        self.button = None
        self.turn = None
        self.board = board
        self.window = Tk()
        self.name = name
        self.points = 0
        self.other_player_points = 0
        self.label = Label(self.window, text=f"{self.name} please wait for your turn"
                           , padx=20, bg="#644a82", fg="#e8dff2",
                           font=("Times New Roman", 20))
        self.connections = Label(self.window, text=f"There are currently no clients"
                                 , padx=20, bg="#5c3e7d", fg="#c4bacf",
                                 font=("Times New Roman", 15))
        self.connections.grid(row=1, column=0)
        self.label.grid(row=0, column=0)
        self.status = True

    def activate_other_gui(self):
        self.connections.destroy()
        score = Frame(self.window)
        self.lpoint = Label(score, text=f"{self.points}", width=2
                            , padx=18
                            , bg="#ddc1e0",
                            fg="#290361")
        self.lpoint.grid(row=4, column=0)
        self.lotherpoint = Label(score, text=f"{self.other_player_points}", width=2
                                 , padx=18
                                 , bg="#ddc1e0"
                                 , fg="#290361")
        self.lotherpoint.grid(row=4, column=1)
        score.grid(row=4, column=2, sticky=SE)
        self.label.config(text=f"{self.name} please wait for your turn")
        wlabel = Label(self.window, text="Already Used Words:",
                       font=("Times New Roman", 15),
                       bg="#ecdded",
                       fg="#240842")
        wlabel.grid(row=5, column=0, sticky=W)

        self.wordlist = Label(self.window, text="",
                              font=("Times New Roman", 15),
                              bg="#38284a", fg="#e8dff2")
        self.wordlist.grid(row=6, column=0, sticky=W)

        self.button = Button(self.window,
                             text='Submit',
                             fg="#36046e",
                             font=("Times New Roman", 15),
                             activeforeground="#36046e",
                             state=DISABLED)
        self.button.grid(row=0, column=2, sticky=W)

        self.entry = Entry(self.window, bg="#e6d3eb", fg="Black")
        self.entry.grid(row=0, column=1, sticky=W)

        self.answer = Label(self.window, text="",
                            font=("Times New Roman", 15),
                            bg="#38284a",
                            fg="#e6d3eb")

        self.answer.grid(row=2, column=1, sticky=SW)

    def __str__(self):
        return self.name

    @staticmethod
    def game_over(lst_players):
        for i in range(len(lst_players)):
            if lst_players[i].status:
                return True
        return False

    @staticmethod
    def scoring(word):
        # 3 - and 4 - letter words are 1 point each
        if len(word) == 4 or len(word) == 3:
            return 1
        # 5-letter words are 2 points each
        if len(word) == 5:
            return 2
        # 6-letter words are 3 points each
        if len(word) == 6:
            return 3
        # 7-letter words are 5 points each
        if len(word) == 7:
            return 5
        # 8-letter words and longer are 11 points each
        if len(word) >= 8:
            return 11

    def reset_points(self):
        self.points = 0
        self.other_player_points = 0
        self.lpoint.config(text=f"{self.points}")
        self.lotherpoint.config(text=f"{self.other_player_points}")

    def add_points(self, points):
        self.points += points
        self.lpoint.config(text=f"{self.points}")

    def add_other_player_points(self, points):
        self.other_player_points = points
        self.lotherpoint.config(text=f"{self.other_player_points}")

    def start_game(self):
        self.window.mainloop()
