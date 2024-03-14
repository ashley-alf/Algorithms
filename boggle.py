import random

from PyDictionary import PyDictionary

from Player import *

# import Game as game

'''
This is module boggle.py

'''
dice = [["A", "E", "A", "N", "E", "G"], ["A", "H", "S", "P", "C", "O"], ["A", "S", "P", "F", "F", "K"],
        ["O", "B", "J", "O", "A", "B"], ["I", "O", "T", "M", "U", "C"], ["R", "Y", "V", "D", "E", "L"],
        ["L", "R", "E", "I", "X", "D"], ["E", "I", "U", "N", "E", "S"], ["W", "N", "G", "E", "E", "H"],
        ["L", "N", "H", "N", "R", "Z"], ["T", "S", "T", "I", "Y", "D"], ["O", "W", "T", "O", "A", "T"],
        ["E", "R", "T", "T", "Y", "L"], ["T", "O", "E", "S", "S", "I"], ["T", "E", "R", "W", "H", "V"],
        ["N", "U", "I", "H", "M", "Qu"]]
dict = PyDictionary()


# Make a 4x4 grid in the form of a 2d list, where each cell contains a randomly selected upper-case character
def new_board():
    return [[random.choice(dice[row * 4 + col]) for col in range(4)] for row in range(4)]


# Print out the board
def board_to_string(other_board):
    s = ""
    for r in range(len(other_board)):
        for letter in other_board[r]:
            s += '[' + letter + '] '
        s = s[:-1]
        s += '\n'
    s = s[:-1]
    return s


def board_has_word(board, word, used_cells=None):
    starting_index = 1
    if used_cells is None:
        # find where the cell(s) containing the first letter is at
        letter = word[0]
        if letter == "Q":
            letter = "Qu"
            starting_index = 2
            starting_cells = cells_with_letter(board, letter)
        else:
            starting_cells = cells_with_letter(board, letter)
        # if the word is not found within the board, return false
        if not starting_cells:
            return False
        # if the letter is found and there are no other letters left,return true
        # this is the base case
        if len(word) == 1:
            return True
        # else, if there are more letters begin the recursive method
        for cell in starting_cells:
            # instantiate used_cells so it is not None
            used_cells = []
            # append the starting cell(s) to the used_cells so we know later on
            # that we cannot use them
            used_cells.append(cell)
            # make a recursive method passing a copy of used_cells (it is not None anymore)
            # and eliminating the first letter of the word
            # if it got through all the letters that were valid on the board return true

            # if board_has_word(board, word[starting_index:], copy.deepcopy(used_cells)):
            if board_has_word(board, word[starting_index:], [cell]):
                return True
            # if none of the neighbors were used to complete the word then...
            return False
    else:
        # store the last item in the used_cells as the current cell
        current_cell = used_cells[-1]
        # get all the possible neighbors
        neighbors = adjacent_cells(current_cell)
        # remove all the used_cells from neighbors
        neighbors = [c for c in neighbors if not c in used_cells]
        # remove all neighbors that don't contain
        # the letter we're looking for (the current first letter)
        neighbors = [x for x in neighbors if board[x[0]][x[1]] == word[0]]
        # at this point, we can check if there are any possibilities remaining
        # and if not, then great, we can't go any further!
        if not neighbors:
            return False
        # if the word has one character remaining
        if len(word) == 1:
            return True
        # continue the recursive method
        for cell in neighbors:
            used_cells.append(cell)
            # same method as above
            # if board_has_word(board, word[starting_index:], copy.deepcopy(used_cells)):
            if board_has_word(board, word[starting_index:], [cell]):
                return True
        # if none of the neighbors were used to complete the word then...
        return False


# check all the adjacent cells of a given a tuple
def adjacent_cells(current_cell):
    # make an empty list
    neighbor_lst = []
    # we can make a nested loop that will check for all the adjacent cells by adding from -1 to 1
    for r in range(-1, 2):
        for c in range(-1, 2):
            # add cells that are less than the length of the board and bigger than 0
            # we can't add the current_cell again, therefore don't add the cell when r and c are 0
            if 0 <= current_cell[0] + r < 4 and 0 <= current_cell[1] + c < 4 and (r, c) != (0, 0):
                # add the cells as a tuple into the list
                neighbor_lst.append((current_cell[0] + r, current_cell[1] + c))
    return neighbor_lst


def cells_with_letter(board, letter):
    # make an empty list
    cell_lst = []
    # traverse through the board
    for r in range(len(board)):
        for c in range(len(board[r])):
            # check if the letter is in the board
            if letter == str(board[r][c]):
                # if so add the coordinates as a tuple into the list
                cell_lst.append((r, c))

    return cell_lst


def console_game_play(board, players):
    total_players = []
    used_words = []
    # Create an object of type Player for each Player
    for p in range(players):
        player = Player(f"PLAYER{p + 1}", board)
        total_players.append(player)
    # Repeat loop until all players have quit
    while Player.game_over(total_players):
        # Only ask players to enter a word if they are still in the game
        for p in total_players:
            if p.status:
                word = input(f"{p.name} please enter a word:\n")
                word = word.upper()
                if word == "Q" or word == 'q':
                    print(f"{p.name} is out of the game")
                    p.status = False
                elif word in used_words:
                    print(f"{p.name}, that word has already been used")
                elif len(word) < 3:
                    print("Word must be at least have 3 letters")
                elif dict.meaning(word, True) is None:
                    print(f"{p.name} that word does not exist")
                # elif dict.meaning(word, True) is not None:
                else:
                    result = board_has_word(board, word)
                    if result:
                        points = Player.scoring(word)
                        if points == 1:
                            print(f"{p.name} you get {points} point")
                        else:
                            print(f"{p.name} you get {points} points")
                        used_words.append(word)
                        p.add_points(points)
                    else:
                        print("That word was not found in the board")
        print(board_to_string(board))

    winner = Player.winner(total_players)
    print(f"Winner is: {winner} with {winner.points} points ")


if __name__ == "__main__":
    board = [["N", "E", "E", "Qu"],
             ["E", "F", "G", "H"],
             ["I", "B", "K", "L"],
             ["A", "B", "C", "D"]]
    players = input("Welcome to the game of Boggle! How many players will play? ")
    print("Let the game begin. Players this is your board: (Press 'Q' to quit) ")
    print(board_to_string(board))
    players = int(players)
    console_game_play(board, 2)
    # game.make_players(1)
    # game.window()
    # game.start()
# game_master(2)
