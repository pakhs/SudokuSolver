from mimetypes import init
import sys
import os
import colorama
from colorama import Fore

def read_board_file():
    file = sys.argv[1]
    file_ext = file.split('.')
    if file_ext[1] != 'board':
        print("Incorrect file type!")
        exit(-1)
    with open(file, "r+") as f:
        contents = f.read()
    contents = contents.split('\n')
    if contents[0] != "#SUDOKU":
        print("Incorrect file structure!")
        exit(-1)
    board = []
    for i in range(9):
        board.append([])
        contents[i+1] = contents[i+1].split(' ')
        for j in range(9):
            board[i].append(int(contents[i+1][j]))
    return board

class Board:
    def __init__(self, board, interactive):
        self.board = board
        self.inter = interactive
    def print(self):
        board = self.board
        print("         SUDOKU BOARD")
        for i in range(len(board)):
            if i % 3 == 0:
                print("-----------------------------")
            for j in range(len(board[i])):
                if j % 3 == 0:
                    print(" | ", end="")
                if j == 8:
                    print(str(board[i][j]) + ' |')
                else:
                    print(str(board[i][j]) + " ", end="")
    def find_next_empty(self):
        b = self.board
        for i in range(len(b)):
            for j in range(len(b[i])):
                if b[i][j] == 0:
                    return (i,j)
        return (-1,-1)
    def checkValid(self, n, position):
        row = position[0]
        col = position[1]

        for j in range(len(self.board[0])):
            if j == col:
                continue
            if self.board[row][j] == n:
                return False
        for i in range(len(self.board[0])):
            if i == row:
                continue
            if self.board[i][col] == n:
                return False
        new_row = (row // 3) * 3
        new_col = (col // 3) * 3

        for i in range(new_row, new_row + 3):
            for j in range(new_col, new_col + 3):
                if self.board[i][j] == n and i != row and j != col:
                    return False
        return True
    def printInSolve(self, position):
        board = self.board
        row = position[0]
        col = position[1]
        print("         SUDOKU BOARD")
        for i in range(len(board)):
            if i % 3 == 0:
                print("-----------------------------")
            for j in range(len(board[i])):
                if j % 3 == 0:
                    print(" | ", end="")
                if j == 8:
                    if (row,col) == (i,j):
                        print(Fore.YELLOW + str(board[i][j]) + Fore.WHITE + ' |')
                    else:
                        print(str(board[i][j]) + ' |')
                else:
                    if (row,col) == (i,j):
                        print(Fore.YELLOW + str(board[i][j]) + Fore.WHITE + " ", end = "")
                    else:
                        print(str(board[i][j]) + " ", end="")
    def solve(self):
        (row,col) = self.find_next_empty()
        if (row,col) == (-1,-1):
            return True
        
        for i in range(1,10):
            if self.checkValid(i, (row,col)):
                self.board[row][col] = i
                if self.inter:
                    os.system("clear")
                    self.printInSolve((row,col))
                    os.system("sleep 0.09")
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False
    def toFile(self):
        f = open("out.board", "w+")
        f.write("#SUDOKU\n")
        for i in range(9):
            for j in range(9):
                if j == 8:
                    f.write(str(self.board[i][j]))
                else:
                    f.write(str(self.board[i][j]) + " ")
            f.write("\n")

    
def main():
    if len(sys.argv) == 3:
        if sys.argv[2] == "True":
            interactive = True
        else:
            interactive = False
    if len(sys.argv) != 3:
        print("Incorrenct command line arguments\nUsage:\npython3 solver.py file.board (True/False)\nTrue/Flase is for interactive solving")
        exit(-1)

    board = Board(read_board_file(), interactive)
    board.print()
    board.solve()
    if interactive:
        os.system("clear")
    board.print()
    board.toFile()

if __name__ == '__main__':
    main()