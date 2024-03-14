from boggle import *
from Player import *
from PyDictionary import PyDictionary

USED_WORDS = []
DICT = PyDictionary()


class Game:
    def __init__(self, name, board):
        self.p = Player(f"Player{name}", board)

    def server_window(self, addr, port):
        self.p.window.title("Boggle")
        self.p.window.configure(background="#38284a")
        self.p.label.config(text=f"Clients can connect to {addr} {port}\n"
                                 f"Game will begin once a connection is made")
    def add_words(self, word):
        USED_WORDS.append(word)
        self.p.wordlist.config(text = f"{USED_WORDS}")
    def check_turn(self):
        return self.p.turn
    def set_turn(self, bool):
        self.p.turn = bool

    def get_points(self):
        return self.p.points

    # def update_server(self, addr):
    #     self.p.connections.config(text=f"Connected to {addr}. You may start the game")
    #     self.p.start_button.config(state=NORMAL, command=self.window)

    def window(self):
        '''
        A display for the grid of letters.
        A display for the scores of both players.
        Something to indicate whose turn it is (Player 1 or Player 2).
        A place to restart the game (i.e. re-shuffle the board, and reset scores to 0).
        Displays for the results of guesses (i.e. success, or failure - "that isn't a valid word!").
        Some way of making a word guess (maybe a text box, or a way of clicking on grid spaces).
        A list of "already used" words (i.e. the successful guesses).
        Display for network connection components (like host IP address / port number -- see below).
        '''
        self.p.activate_other_gui()

        self.p.window.title("Boggle")
        self.p.window.configure(background="#38284a")
        table = Label(self.p.window, text="Score\n You vs Opponent",
                      bg="#9799ba",
                      font=("Times New Roman", 15),
                      fg="#ece4f5")
        table.grid(row=3, column=2, sticky=SW)

        frame = Frame(self.p.window)
        # l = Label(self.p.window, text="", bg="#38284a")
        # l.grid(row=2, column=0)
        frame.grid(row=3, column=0, sticky=W)
        for x in range(4):
            for y in range(4):
                l = Label(frame, text=f"{self.p.board[y][x]}",
                          width=2,
                          relief=SUNKEN,
                          bd=7,
                          # bg = "#81a4f7",
                          fg="#290361",
                          bg="#c1a4eb",
                          font=("Times New Roman", 40, 'bold'))
                l.grid(row=y, column=x)



    def player_turn(self):
        self.p.turn = True
        self.p.answer.config(text="" )

        self.p.label.config(text=f"{self.p.name} it is your turn! Enter a word:")

        self.p.button.grid(row=0, column=2, sticky=W)

        self.p.button.config(command=self.check_word, state=NORMAL)


    def check_word(self):
        word = self.p.entry.get()
        word = word.upper()
        print("Word", word)
        if word == "Q" or word == 'q':
            self.p.answer.config(text=f"{self.p.name} is out of the game")
            self.p.status = False
            self.change_gui()
        if word in USED_WORDS:
            self.p.answer.config(text=f"{self.p.name} that word has already been used")
            self.change_gui()
        elif len(word) < 3:
            self.p.answer.config(text="Word must be at least 3 letters long",)
            self.change_gui()

        elif DICT.meaning(word, True) is None:
            self.p.answer.config(text=f"That word does not exist")
            self.change_gui()

        else:
            result = board_has_word(self.p.board, word)
            if result:
                points = Player.scoring(word)
                if points == 1:
                    self.p.answer.config(text=f"You get {points} point")
                    self.p.word = word
                else:
                    self.p.answer.config(text=f"You get {points} points" )
                    self.p.word = word

                self.p.add_points(points)

                USED_WORDS.append(word)
                self.p.wordlist.config(text= f"{USED_WORDS}")
                self.change_gui()
            else:
                self.p.answer.config(text="That word was not found in the board")
                self.change_gui()


    def change_gui(self):
        self.p.turn = False
        self.p.label.config(text=f"{self.p.name} please wait for your turn")
        self.p.button.config(state=DISABLED)


    def get_word(self):
        return self.p.word


    def start(self):
        self.p.start_game()

    def reset_update(self):
        global USED_WORDS
        USED_WORDS = []
        self.p.wordlist.config(text = "")
        self.p.answer.config(text = "")
        self.p.points = 0
        self.p.other_player_points = 0
        self.window()

