import time
import keys
import math
import random
from keys import send_key
line = []

def get_line():
    with open("board_state.csv", mode="r")as file:
        for each_line in file:
            for char in each_line.split(","):
                line.append(char)
    pass

def main():
    LEFT = 0
    DOWN = 0
    RIGHT = 0
    BEST_MOVE = None
    get_line()
    board_size = int(math.sqrt(len(line)))
    board = [[random.randint(0,9)] * board_size for _ in range(0,board_size)]
    for y in range(0,board_size):
        for x in range(0,board_size):
            board[y][x] =int(line[x + (y * board_size)])
    def value(list):
        print(list)
        val = 1
        for x in list:
            try:
                if list[x] == list[x+1]:
                    val += 2*list[x]
            except IndexError:
                continue
        return val

    def getCell(x, y):
        """return the cell value at x,y"""
        return board[y][x]

    def getLine(y):
        """return the y-th line, starting at 0"""
        return board[y]

    def getCol(x):
        """return the x-th column, starting at 0"""
        return [getCell(x, i) for i in range(0,board_size)]

    for num in range(0,board_size):
        DOWN += value(getLine(num))

    for num in range(0,board_size):
        LEFT += value(getCol(num))
        RIGHT += value(getCol(num))

    # print(board_size)
    # print(line)
    print("LEFT:",LEFT,"DOWN:",DOWN,"RIGHT:",RIGHT)
    print(board)


    pass
if __name__ == '__main__':
    main()
