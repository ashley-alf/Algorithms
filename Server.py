import threading
from functools import partial

from Client import *
from Player import *

BOARD = new_board()


class Server:
    def __init__(self, addr, port):
        self.turn = None
        self.s = None
        self.player = None
        self.a = addr
        self.p = port
        self.points = 0
        self.start_server()
        self.send_message = True

    def start_server(self):
        self.s = socket.socket()
        self.s.bind((self.a, self.p))
        self.s.listen(10)
        t = threading.Thread(target=self.accept_connections, args=(), daemon=True)
        t.start()
        self.player = Game("1", BOARD)
        self.player.server_window(self.a, self.p)
        self.player.start()

    def accept_connections(self):
        conn, addr = self.s.accept()
        self.player.window()
        self.player.p.reset_button = Button(self.player.p.window,
                                            text="Reset",
                                            fg="#36046e",
                                            font=("Times New Roman", 15),
                                            activeforeground="#36046e",
                                            command=partial(self.reset, conn),
                                            state=DISABLED)
        self.player.p.reset_button.grid(row=5, column=2, sticky=E)
        b = pickle.dumps(BOARD)
        conn.send(b)
        self.game_play(conn)
        # t2 = threading.Thread(target=self.game_play, args=(conn,), daemon=True)
        # t2.start()

    def game_play(self, conn):
        while True:
            answer = conn.recv(1080)
            try:
                info = pickle.loads(answer)
            except pickle.UnpicklingError:
                # Method that allows the Server GUI to submit a word
                # By the end of this method the self.turn changes to False
                self.player.player_turn()
                self.turn = self.player.check_turn()
                self.player.p.reset_button.config(state=NORMAL)
                while self.turn:
                    self.turn = self.player.check_turn()
                self.check_points(conn)

            else:
                self.player.add_words(info[1])
                self.player.p.add_other_player_points(info[0])
                self.player.player_turn()
                self.turn = self.player.check_turn()
                self.player.p.reset_button.config(state=NORMAL)
                while self.turn:
                    self.turn = self.player.check_turn()
                self.check_points(conn)

    def check_points(self, conn):
        self.player.p.reset_button.config(state=DISABLED)
        if self.player.get_points() > self.points:
            self.points = self.player.get_points()
            word = self.player.get_word()
            print("word guess: ", word)
            print("Used words:", USED_WORDS)
            l = [self.points, word]
            info = pickle.dumps(l)
            conn.send(info)
            print("list sent")
        elif self.send_message:
            conn.send("start".encode())
            print("message sent")
        elif not self.send_message:
            self.send_message = True


    def reset(self, conn):
        global BOARD
        self.player.p.turn = False
        BOARD = new_board()
        self.player.p.board = BOARD
        self.points = 0
        self.player.p.reset_button.config(state=DISABLED)
        self.player.p.label.config(text=f"{self.player.p.name} please wait for your turn")
        self.player.p.button.config(state=DISABLED)
        self.send_message = False
        self.player.reset_update()
        l = ["reset", BOARD]
        info = pickle.dumps(l)
        conn.send(info)
        print("new board sent")
