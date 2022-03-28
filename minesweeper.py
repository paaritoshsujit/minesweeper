
############################################################################
##### Implemtation of the game MineSweeper, using classes and recursion ####
############################################################################

import random
import re


class Board:
    def __init__(self, dim_size, num_bombs):
        # we keep track of these parameters since they will be of use later
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # lets create the board
        self.board = self.make_new_board()  # helper function
        self.assign_values_to_board()       # we assign each square with the number of neighbouring bombs

        # initialize a set to keep track of the locations we've uncovered
        # we'll save (row, column) tuples into this set
        self.dug = set()

    def make_new_board(self):
        # we create a board based on the dimensions and bombs 
        # we construct  a list of lists here to create the 2-D board

        # generate a new board
        board =[[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # this creates an array of size dim_size x dim_size, where each element is None

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':      # We use '*' to represent a bomb
                # this means that we already planted a bomb in this location, so instead we kep going
                continue

            # if the location does not have a bomb in its location
            board[row][col] = '*'
            bombs_planted += 1

        return board

    def assign_values_to_board(self):   # after the bombs are planted we assign a number (between 0 and 8) for all the empty spaces, which
                                        # represents how many neighbouring bombs there are. Storing these values early on helps save us time and
                                        # computational power, since we won't have to compute it at each iteration if we have the values already.
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_neighbouring_bombs(r,c)
            

    def get_neighbouring_bombs(self, row , col):

        num_neighbouring_bombs = 0
        for r in range( max(0, row - 1) ,  min(self.dim_size - 1, (row + 1)) + 1):    # It is also important not to go out of bounds, hence max and 
            for c in range( max(0, col - 1), min(self.dim_size - 1, (col + 1)) + 1):
                if r == row and c == col:   # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1
        
        return num_neighbouring_bombs

    def dig(self, row, col):    # function used to dig in a specific location

        # return True if successful and False if not

        # There are a few scenarios:
        #                           1. Dig at bomb -> game over 
        #                           2. Dig at location w neighbouting bombs -> finish dig
        #                           3. Dig at location w no neighbouring bombs -> recursively dig neighbours

        self.dug.add((row, col)) # to keep track of dig location

        if self.board[row][col] == '*':
            return False    # game over
        elif self.board[row][col] > 0:  # i.e. neighbouring bombs exist
            return True     # finish dig
        
        # self.board[row][col] == 0
        for r in range(max(0,row - 1) ,  min(self.dim_size - 1, (row + 1)) + 1):    
            for c in range(max(0, col - 1), min(self.dim_size - 1, (col + 1)) + 1):
                if (r, c) in self.dug:
                    continue    # if the location has already been dug up, we go for the next iteration
                
                self.dig(r,c)   # if not dug up, we perform the digging action on that square
        
        # if our initial dig didn't hit a bomb, we shouldnt hit a bomb here
        return True

    def __str__(self):  # this is a magic function, if you call print print on this object, it will print out what this function returns
        
        # first we create a new board in the form of an array which represents what the user would see
        visible_board = [[None for  _ in range(self.dim_size)] for _ in range(self.dim_size)]

        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:      # if we have dug previously at this location, then we display the value of the square
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '   # if we havent dug, we dont know whats there, and leave the square blank

        # now we need to put the entire visible board into the form of a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

#  play the game
def play(dim_size = 10 , num_bombs = 10):

    # Step 1 : create the board and plant the mines
    board = Board(dim_size, num_bombs)


    while len(board.dug) < board.dim_size**2 - num_bombs:   # ends if game over, or all squares are dug which are not bombs
        print(board)
        # Step 2 : show the user the board and ask where they want to dig
        user_input = re.split(',(\\s)*' ,input('Where would you like to dig? Input as row, col: '))   # eg '0, 3'

        row, col = int(user_input[0]), int(user_input[-1])

        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size: # check for invalid input
            print("Invalid Location, Out of Bounds! Try again.")
            continue

        # Step 3 : if location is a mine, show game over
        #          if not, dig recursively until each square is next to a bomb
        # if valid, then we dig
        safe = board.dig(row, col)     # recall that this function returns True if its safe to dig, and False if its game over
        if not safe:    # dug a bomb
            break       # game over
        
        # Step 4 : loop until game reaches any one of the two end conditions
        
    # we check how the while loop was exited, ie was bomb dug or was game completed
    if safe:
        print('Congratulations! You Win!')
    else:
        print('Sorry Game Over :(')
        # we can also reveal all the whole board
        board.dug = [(r,c) for r in range(dim_size) for c in range(dim_size)]   # this says we dug all the locations in the board
        print(board)    # since every square is dug, all the values are shown on the board


if __name__ == '__main__':
    play()