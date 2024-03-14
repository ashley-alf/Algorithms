import pickle
import socket
import threading
from Game import *


class Client:
    def __init__(self, addr, port):
        self.s = None
        self.a = addr
        self.p = port
        self.board = None
        self.turn = None
        self.player = None
        self.answer = None
        self.points = 0
        self.start_client()

    def start_client(self):
        self.s = socket.socket()
        self.s.connect((self.a, self.p))
        self.answer = self.s.recv(1080)
        self.board = pickle.loads(self.answer)
        self.player = Game("2", self.board)
        self.player.window()
        t = threading.Thread(target=self.communication, args=(), daemon=True)
        t.start()

        self.player.start()


    def communication(self):
        self.s.send("start".encode())
        print("message sent")
        while True:
            answer = self.s.recv(1080)
            try:
                info = pickle.loads(answer)
            except pickle.UnpicklingError:
                if answer.decode() == "start":
                    print("Received from Server", answer.decode())
                    # Method that allows this GUI to guess a word
                    self.player.player_turn()
                    self.turn = self.player.check_turn()
                    while self.turn:
                        self.turn = self.player.check_turn()
                    self.check_points()
                    print("message sent")
            else:
                if info[0] == "reset":
                    print("board received")
                    self.player.p.board = info[1]
                    self.points = 0
                    self.player.reset_update()
                    self.player.player_turn()
                    self.turn = self.player.check_turn()
                    while self.turn:
                        self.turn = self.player.check_turn()
                    self.check_points()

                else:
                    self.player.add_words(info[1])
                    self.player.p.add_other_player_points(info[0])

                    self.player.player_turn()
                    self.turn = self.player.check_turn()
                    while self.turn:
                        self.turn = self.player.check_turn()
                    self.check_points()

    def check_points(self):
        if self.player.get_points() > self.points:
            self.points = self.player.get_points()
            word = self.player.get_word()
            t = [self.points, word]
            info = pickle.dumps(t)
            self.s.send(info)
            print("list sent")
        else:
            self.s.send("start".encode())
            print("message sent")


