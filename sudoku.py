from copy import deepcopy
from time import sleep
import math
import random
import sys
import timeit


class Board:
    def __init__(self, difficulty):
        self.final = [[0 for x in range(9)] for y in range(9)]
        self.failure = 0
        while not self.generate():
            self.clear()
        self.prepare(difficulty)
    
    def generate(self):
        for i in range(1,10):
            while self.count_final(i) < 9:
                for x in range(9):
                    y = random.randint(0,8)
                    attempts = 0
                    while self.final[x][y] != 0 or not self.checkPlacement(x, y, i):
                        attempts += 1
                        y = random.randint(0,8)
                        if attempts > 20:
                            self.failure += 1
                            return False
                    self.final[x][y] = i
        return True
    
    def count_final(self, value):
        i = 0
        for x in range(9):
            for y in range(9):
                if self.final[x][y] == value:
                    i += 1
        return i
    
    def count(self, value):
        i = 0
        for x in range(9):
            for y in range(9):
                if self.active[x][y] == value:
                    i += 1
        return i
        
    def validate(self):
        for x in range(9):
            for y in range(9):
                if self.final[x][y] != self.active[x][y]:
                    return False
        return True
    
    def clear(self):
        self.final = [[0 for x in range(9)] for y in range(9)]
    
    def checkPlacement(self, x, y, value):
        box_x = x//3*3
        box_y = y//3*3
        for a in range(box_x, box_x+3):
            for b in range(box_y, box_y+3):
                if self.final[a][b] == value:
                    return False
        for a in range(9):
            if a >= box_x and a < box_x + 3:
                continue
            if self.final[a][y] == value:
                return False
        for b in range(9):
            if b >= box_y and b < box_y + 3:
                continue
            if self.final[x][b] == value:
                return False
        return True
    
    def prepare(self, difficulty):
        self.active = deepcopy(self.final)
        difficulty = min(difficulty, 4)
        difficulty = max(difficulty, 1)
        for i in range(difficulty+3):
            removed = 0
            while removed < 9:
                x = random.randint(0,8)
                y = random.randint(0,8)
                if self.active[x][y] != 0:
                    self.active[x][y] = 0
                    removed += 1
        
    def get(self, x, y):
        return self.active[x][y] if self.active[x][y] > 0 else ' '
        
    def __str__(self):
        out = "  "
        for x in range(9):
            if x % 3 == 0:
                out += "|-------|-------|-------|\n  "
            for y in range(3):
                out += f'| {self.get(x,y*3)} {self.get(x,y*3+1)} {self.get(x,y*3+2)} '
            out += "|\n  "
        out += "|-------|-------|-------|"
    
        return out


def main():
    print(f'  |{"-"*23}|\n  |{"Sudoku":^23s}|\n  |{"Created by TheKDub":^23s}|\n  |{"-"*23}|\n')
    board = Board(int(sys.argv[1]) if len(sys.argv) > 1 else int(input("Enter a difficulty (1 [Easy] - 4 [Hard]): ")))
    print(f'  Solved? {board.validate()}\n{board}')
    while not board.validate():
        try:
            x = int(input("\n  Row: "))
            y = int(input("  Col: "))
            v = int(input("  Val: "))
            if input(f'    Is {v} at {x}, {y} correct? (y/n) ').lower() != 'y':
                continue
            board.active[x-1][y-1] = v
            print(f'  Solved? {board.validate()}\n{board}')
        except ValueError:
            print('  Invalid input, try again!')
    print("\n  Congrats! You've solved Sudoku!")


main()
