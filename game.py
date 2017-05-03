# -*- coding: UTF-8 -*-
from __future__ import print_function

import atexit
import os
import os.path
import math
import sys

from colorama import init, Fore, Style
import keypress
from board import Board

init(autoreset=True)


class Game(object):
    """
    A 2048 game
    """

    __dirs = {
        keypress.UP: Board.UP,
        keypress.DOWN: Board.DOWN,
        keypress.LEFT: Board.LEFT,
        keypress.RIGHT: Board.RIGHT,
        keypress.SPACE: Board.PAUSE,
        keypress.UNDO: Board.UNDO,
    }

    __is_windows = os.name == 'nt'

    COLORS = {
        2 ** 0: Fore.GREEN, 2 ** 1: Fore.BLUE + Style.BRIGHT, 2 ** 2: Fore.CYAN, 2 ** 3: Fore.RED,
        2 ** 4: Fore.MAGENTA, 2 ** 5: Fore.CYAN, 2 ** 6: Fore.BLUE + Style.BRIGHT, 2 ** 7: Fore.MAGENTA,
        2 ** 8: Fore.GREEN, 2 ** 9: Fore.RED, 2 ** 10: Fore.YELLOW, 2 ** 11: Fore.RED,
        2 ** 12: Fore.CYAN, 2 ** 13: Fore.GREEN, 2 ** 14: Fore.BLUE + Style.BRIGHT, 2 ** 15: Fore.CYAN,
        2 ** 16: Fore.RED, 2 ** 17: Fore.MAGENTA, 2 ** 18: Fore.CYAN, 2 ** 19: Fore.BLUE + Style.BRIGHT,
        2 ** 20: Fore.MAGENTA, 2 ** 21: Fore.GREEN, 2 ** 22: Fore.RED, 2 ** 23: Fore.YELLOW,
        2 ** 24: Fore.RED, 2 ** 25: Fore.CYAN, 2 ** 26: Fore.GREEN, 2 ** 27: Fore.BLUE + Style.BRIGHT,
        2 ** 28: Fore.CYAN, 2 ** 29: Fore.RED, 2 ** 30: Fore.MAGENTA, 2 ** 31: Fore.BLUE + Style.BRIGHT,
        2 ** 32: Fore.CYAN, 2 ** 33: Fore.RED, 2 ** 34: Fore.MAGENTA, 2 ** 35: Fore.CYAN,
        2 ** 36: Fore.BLUE + Style.BRIGHT, 2 ** 37: Fore.MAGENTA, 2 ** 38: Fore.GREEN, 2 ** 39: Fore.RED,
        2 ** 40: Fore.RED, 2 ** 41: Fore.BLUE + Style.BRIGHT, 2 ** 42: Fore.CYAN, 2 ** 43: Fore.RED,
        2 ** 44: Fore.MAGENTA, 2 ** 45: Fore.CYAN, 2 ** 46: Fore.BLUE + Style.BRIGHT, 2 ** 47: Fore.MAGENTA,
        2 ** 48: Fore.GREEN, 2 ** 49: Fore.RED, 2 ** 50: Fore.RED, 2 ** 51: Fore.BLUE + Style.BRIGHT,
        2 ** 52: Fore.CYAN, 2 ** 53: Fore.RED, 2 ** 54: Fore.MAGENTA, 2 ** 55: Fore.CYAN,
        2 ** 56: Fore.BLUE + Style.BRIGHT, 2 ** 57: Fore.MAGENTA, 2 ** 58: Fore.GREEN, 2 ** 59: Fore.RED,
        2 ** 60: Fore.RED, 2 ** 61: Fore.BLUE + Style.BRIGHT, 2 ** 62: Fore.CYAN, 2 ** 63: Fore.RED,
        2 ** 64: Fore.MAGENTA, 2 ** 65: Fore.CYAN, 2 ** 66: Fore.BLUE + Style.BRIGHT, 2 ** 67: Fore.MAGENTA,
        2 ** 68: Fore.GREEN, 2 ** 69: Fore.RED, 2 ** 70: Fore.RED, 2 ** 71: Fore.BLUE + Style.BRIGHT,
        2 ** 72: Fore.CYAN, 2 ** 73: Fore.RED, 2 ** 74: Fore.MAGENTA, 2 ** 75: Fore.CYAN,
        2 ** 76: Fore.BLUE + Style.BRIGHT, 2 ** 77: Fore.MAGENTA, 2 ** 78: Fore.GREEN, 2 ** 79: Fore.RED,
        2 ** 80: Fore.RED, 2 ** 81: Fore.BLUE + Style.BRIGHT, 2 ** 82: Fore.CYAN, 2 ** 83: Fore.RED,
        2 ** 84: Fore.MAGENTA, 2 ** 85: Fore.CYAN, 2 ** 86: Fore.BLUE + Style.BRIGHT, 2 ** 87: Fore.MAGENTA,
        2 ** 88: Fore.GREEN, 2 ** 89: Fore.RED,
    }

    # see Game#adjustColors
    # these are color replacements for various modes
    __color_modes = {
        'dark': {
            Fore.BLUE: Fore.WHITE,
            Fore.BLUE + Style.BRIGHT: Fore.WHITE,
        },
        'light': {
            Fore.YELLOW: Fore.BLACK,
        },
    }

    # SCORES_FILE = '%s/.term2048.scores' % os.path.expanduser('~')
    # STORE_FILE = '%s/.term2048.store' % os.path.expanduser('~')

    SCORES_FILE = 'cmd2048_scores.txt'
    STORE_FILE = 'cmd2048_store.txt'

    def __init__(self, scores_file=SCORES_FILE, colors=COLORS,
                 store_file=STORE_FILE, clear_screen=True,
                 mode=None, azmode=False, element_mode=False, **kws):
        """
        Create a new game.
            scores_file: file to use for the best score (default
                         is ~/.term2048.scores)
            colors: dictionnary with colors to use for each tile
            store_file: file that stores game session's snapshot
            mode: color mode. This adjust a few colors and can be 'dark' or
                  'light'. See the adjustColors functions for more info.
            other options are passed to the underlying Board object.
        """
        self.board = Board(**kws)
        self.score = 0
        self.scores_file = scores_file
        self.store_file = store_file
        self.clear_screen = clear_screen

        self.__colors = colors
        self.__azmode = azmode
        self.__element_mode = element_mode

        self.loadBestScore()
        self.adjustColors(mode)

    def adjustColors(self, mode='dark'):
        """
        Change a few colors depending on the mode to use. The default mode
        doesn't assume anything and avoid using white & black colors. The dark
        mode use white and avoid dark blue while the light mode use black and
        avoid yellow, to give a few examples.
        """
        rp = Game.__color_modes.get(mode, {})
        for k, color in self.__colors.items():
            self.__colors[k] = rp.get(color, color)

    def loadBestScore(self):
        """
        load local best score from the default file
        """
        try:
            with open(self.scores_file, 'r') as f:
                self.best_score = int(f.readline(), 10)
        except Exception:
            self.best_score = 0
            return False
        return True

    def saveBestScore(self):
        """
        save current best score in the default file
        """
        if self.score > self.best_score:
            self.best_score = self.score
        try:
            with open(self.scores_file, 'w') as f:
                f.write(str(self.best_score))
        except Exception:
            return False
        return True

    def incScore(self, pts):
        """
        update the current score by adding it the specified number of points
        """
        self.score += pts
        if self.score > self.best_score:
            self.best_score = self.score

    def readMove(self):
        """
        read and return a move to pass to a board
        """
        k = keypress.getKey()
        return Game.__dirs.get(k)

    def store(self):
        """
        save the current game session's score and data for further use
        """
        size = self.board.SIZE
        cells = []

        for i in range(size):
            for j in range(size):
                cells.append(str(self.board.getCell(j, i)))

        score_str = "%s\n%d" % (' '.join(cells), self.score)

        try:
            with open(self.store_file, 'w') as f:
                f.write(score_str)
        except:
            return False
        return True

    def restore(self):
        """
        restore the saved game score and data
        """

        size = self.board.SIZE

        try:
            with open(self.store_file, 'r') as f:
                lines = f.readlines()
                score_str = lines[0]
                self.score = int(lines[1])
        except Exception:
            return False

        score_str_list = score_str.split(' ')
        count = 0

        for i in range(size):
            for j in range(size):
                value = score_str_list[count]
                self.board.setCell(j, i, int(value))
                count += 1

        return True

    def clearScreen(self):
        """Clear the console"""
        if self.clear_screen:
            os.system('cls' if self.__is_windows else 'clear')
        else:
            print('\n')

    def hideCursor(self):
        """
        Hide the cursor. Don't forget to call ``showCursor`` to restore
        the normal shell behavior. This is a no-op if ``clear_screen`` is
        falsy.
        """
        if not self.clear_screen:
            return
        if not self.__is_windows:
            sys.stdout.write('\033[?25l')

    def showCursor(self):
        """Show the cursor."""
        if not self.__is_windows:
            sys.stdout.write('\033[?25h')

    def loop(self):
        """
        main game loop. returns the final score.
        """
        pause_key = self.board.PAUSE
        undo_key = self.board.UNDO
        margins = {'left': 4, 'top': 4, 'bottom': 4}

        atexit.register(self.showCursor)

        try:
            self.hideCursor()
            while True:
                self.clearScreen()
                print(self.__str__(margins=margins))
                if self.board.won() or not self.board.canMove():
                    break
                m = self.readMove()
                if (m == pause_key):
                    self.saveBestScore()
                    if self.store():
                        print("Game successfully saved. "
                              "Resume it with `cmd2048 --resume`.")
                        return self.score
                    print("An error occurred while saving your game.")
                    return
                if m == undo_key:
                    self.board.load_from_history()
                    continue
                else:
                    self.incScore(self.board.move(m))
                    self.board.export_board_state()
                    self.board.load_to_history()
        except KeyboardInterrupt:
            self.saveBestScore()
            return
        self.saveBestScore()
        print('You won!' if self.board.won() else 'Game Over')
        return self.score

    def getCellStr(self, x, y):  # TODO: refactor regarding issue #11
        """
        return a string representation of the cell located at x,y.
        """
        c = self.board.getCell(x, y)

        if c == 0:
            if self.__azmode:
                return '.'
            if self.__element_mode:
                return '  .'
            else:
                return '.'
        # TODO classify (COLOUR) according to period of element
        elif self.__element_mode:
            elements = ["H", "He",
                        "Li", "Be", "B", "C", "N", "O", "F", "Ne",
                        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
                        "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
                        "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
                        "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
                        "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Ti", "Pb", "Bi", "Po", "At", "Rn",
                        "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No",
                        "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Uut", "Fi", "Uup", "Lv", "Uus", "Uuo"]
            s = elements[int(math.log(c, 2)) - 1]
            if len(s) == 1:
                return self.__colors.get(c, Fore.RESET) + '  ' + s + Style.RESET_ALL
            elif len(s) == 2:
                return self.__colors.get(c, Fore.RESET) + ' ' + s + Style.RESET_ALL
            else:
                return self.__colors.get(c, Fore.RESET) + s + Style.RESET_ALL

        elif self.__azmode:
            az = {}
            for i in range(1, int(math.log(self.board.goal(), 2))):
                az[2 ** i] = chr(i + 96)

            if c not in az:
                return '?'
            s = az[c]
        elif c == 1024:
            s = ' 1k'
        elif c == 2048:
            s = ' 2k'
        else:
            s = '%3d' % c

        return self.__colors.get(c, Fore.RESET) + s + Style.RESET_ALL

    def boardToString(self, margins={}):
        """
        return a string representation of the current board.
        """
        b = self.board
        rg = range(b.size())
        left = '  ' * margins.get('left', 0)
        s = '\n\n'.join(
            [left + ' '.join([self.getCellStr(x, y) for x in rg]) for y in rg])
        return s

    def __str__(self, margins={}):
        b = self.boardToString(margins=margins)
        top = '\n' * margins.get('top', 0)
        bottom = '\n' * margins.get('bottom', 0)
        scores = ' ' * \
            margins.get(
                'left', 0) + '  Score: %5d  Best: %5d\n\n' % (self.score, self.best_score)
        return top + scores + b + bottom
