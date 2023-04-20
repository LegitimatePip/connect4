#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 12:44:39 2021

@author: pipjackson
"""
import time
import sys
import re
import os
import numpy as np

if os.name == "nt":
    clear = lambda: os.system("cls")
else:
    clear = lambda: os.system("clear")


class Board():
    def __init__(self, height=6, width=7, match_length=4):
        self.H = height
        self.W = width
        self.M = match_length
        self.board = np.zeros((height, width), dtype=int)
        self.available_columns = np.arange(self.W)
        self.player_1_turn = True
        self.col_separator = "|"
    def __str__(self):
        piece =  {0: '.', 1: 'X', -1: 'O'}
        return "\n".join(
            [f"{self.col_separator}".join(row) for row in
             np.array(
                [piece[e] for e in self.board.flatten()]
                )
                .reshape((self.H,self.W))])
    def addPiece(self, col):
        if self.board[:, col].all():
            raise ValueError("Column full")
        self.board[
            np.where(self.board[:,col] ==0)[0][-1],
            col
            ] = 2 * self.player_1_turn - 1
        self.player_1_turn = not self.player_1_turn
        self.available_columns = np.where(
            ~ self.board.all(axis=0),
            self.available_columns,
            -1)
    def checkWin(self, find_winner=False):
        horizontal = np.sum(
            [self.board[:,
                        i : self.W - self.M + i+1]
             for i in np.arange(self.M)],
                       axis = 0
                       )
        vertical = np.sum(
            [self.board[i : self.H - self.M + i+1,
                        :]
             for i in np.arange(self.M)],
                       axis = 0
                       )
        # diagonal0 is top-left to bottom-right
        diagonal0 = np.sum(
            [self.board[i : self.H - self.M + i+1,
                        i : self.W - self.M + i+1]
             for i in np.arange(self.M)],
                       axis = 0
                       )
        # diagonal1 is bottom-left to top-right
        diagonal1 = np.sum(
            [self.board[i : self.H - self.M + i+1,
                        self.M - i-1 : self.W - i]
             for i in np.arange(self.M)],
                       axis = 0
                       )
        directions = [horizontal, vertical, diagonal0, diagonal1]
        full_array = np.concatenate(
            [direction.flatten() for direction in directions])
        if find_winner:
            return np.sign(
                full_array[np.argwhere(np.abs(full_array) == self.M)[0]])
        return np.any(np.abs(full_array) == self.M)

class Connect4():
    def __init__(self, height=6, width=7, match_length=4):
        self.H = height
        self.W = width
        self.M = match_length
        self.board = Board(self.H, self.W, self.M)
        self.start_index_at_1 = True
    def switchStartIndex(self):
        self.start_index_at_1 = not self.start_index_at_1
    def displayColumns(self):
        a = np.where(
            np.arange(self.board.W) in self.board.available_columns,
            self.board.available_columns + self.start_index_at_1,
            "_")
        print(f"{self.board.col_separator}".join(a))
    def displayBoard(self):
        print(f"\n{self.board}\n")
    def playMove(self, col):
        self.board.addPiece(col - self.start_index_at_1)
    def inputMove(self):
        num_format = re.compile(r"^-?\d+$")
        column = -1
        while not num_format.match(str(column))\
            or int(column) not in\
            self.board.available_columns + self.start_index_at_1\
            or column == -1:
            column = input("Please type the column\n")
            print("\nSorry - that column doesn't work\n")
        self.playMove(int(column))
    def endGame(self):
        yes_p = re.compile(r"[Yy].*")
        no = re.compile(r"[Nn].*")
        clear()
        print("\n\n")
        self.displayBoard()
        if self.board.checkWin(find_winner=True) == 1:
            print("Player 1 wins!")
        else:
            print("Player 2 wins!")
        while True:
            response = input("\nPlay another game? (Y/N)\n")
            if yes_p.match(response):
                self.board = Board(self.H, self.W, self.M)
                self.playGame()
            elif no.match(response):
                sys.exit()
            else:
                print("Sorry - response not understood")
    def playGame(self):
        while not self.board.checkWin():
            clear()
            print("\n\n")
            if self.board.player_1_turn:
                print("Player 1's turn! (X)")
            else:
                print("Player 2's turn! (O)")
            self.displayBoard()
            self.displayColumns()
            self.inputMove()
        self.endGame()

if __name__ == "__main__":
    start_time = time.time()
    game = Connect4()
    game.playGame()
    print(f"{time.time() - start_time} seconds".center(40, "-"))
