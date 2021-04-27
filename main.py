import pygame as pg
import random
import basicminimax as minimax
import numpy as np


class Board:
    def __init__(self, isGPUenabled=False, gridsize=5):
        self.BLOCKSIZE = 60
        self.GRIDSIZE = gridsize
        self.SCREENWIDTH = 800
        self.SCREENHEIGHT = 600
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.pointpositiondict = {}
        self.linepositiondict = {}
        self.squareposition = {}
        self.playerAmoves = []  # .. Random.. Stores Lineposition value
        self.playerBmoves = []  # .. AI.. Stores Lineposition value
        self.playerAScore = 0
        self.playerBScore = 0
        self.availableStates = [i for i in range(1, ((self.GRIDSIZE - 1) * self.GRIDSIZE * 2) + 1)]
        self.visitedNodes = []  # .. stores all visited nodes by both players
        self.visitedPositionNodes = np.zeros(len(self.availableStates), dtype=int)
        self.playerAPosition = []
        self.playerBPosition = []
        self.screen = None
        self.whoseMove = 0  # .. 0 => playerA (random player)  1=> playerB (AI player)
        self.outputfilename = "playerMovesData.txt"
        self.file = open(self.outputfilename, "a+")
        self.isGPUenabled = isGPUenabled

    def intialize_board(self):
        pg.init()
        self.screen = pg.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        pg.display.set_caption("Dot Square Game")
        self.screen.fill((0, 128, 255))

    def drawGrid(self):
        center = (90, 20)
        radius = 6
        counter = 1
        for x in range(self.GRIDSIZE):
            for y in range(self.GRIDSIZE):
                result = (y * self.BLOCKSIZE + center[0], x * self.BLOCKSIZE + center[1])
                pg.draw.circle(self.screen, (0, 0, 0), result, radius)
                # print(result)
                self.pointpositiondict[counter] = result
                counter += 1
        # print("pointpositiondict {}".format(self.pointpositiondict))

    def constructLinePos(self):
        value = ((self.GRIDSIZE - 1) * self.GRIDSIZE)
        increment = 1
        for i in range(1, value + 1):
            if i > (self.GRIDSIZE - 1) and (i - 1) % (self.GRIDSIZE - 1) == 0:
                increment += 1
            self.linepositiondict[i] = (1 + (increment - 1), 2 + (increment - 1))
            increment += 1

        increment = 1
        for i in range(value + 1, value * 2 + 1):
            self.linepositiondict[i] = (1 + (increment - 1), self.GRIDSIZE + 1 + (increment - 1))
            increment += 1

        # print("linepositiondict {}".format(self.linepositiondict))

    def drawLine(self, linePosition, color):
        pointposition = self.linepositiondict[linePosition]
        # print(f"pointposition {pointposition}")
        # print(f"pointposition dict {self.pointpositiondict[pointposition[0]]}")
        # print(f"pointposition dict {self.pointpositiondict[pointposition[1]]}")
        pg.draw.line(self.screen, color, start_pos=self.pointpositiondict[pointposition[0]],
                     end_pos=self.pointpositiondict[pointposition[1]], width=3)

    def constructSquares(self):
        increment = 0
        for i in range(1, (self.GRIDSIZE - 1) ** 2 + 1):
            # print(i)
            if i > 2 and (i - 1) % (self.GRIDSIZE - 1) == 0:
                increment += 1
            self.squareposition[i] = (i, i + (self.GRIDSIZE - 1), i + increment + (self.GRIDSIZE - 1) * self.GRIDSIZE,
                                      i + increment + (self.GRIDSIZE - 1) * self.GRIDSIZE + 1)
        # print("squareposition {}".format(self.squareposition))

    def checkSquareFormed(self, playerMoves, currentMove=1, player=""):
        if len(playerMoves) >= 4:
            squareformed = True
            # print(f"playerMoves {playerMoves} and currentMove {currentMove} by player {player} {self.squareposition.items()}")
            for key, value in self.squareposition.items():
                # print(f"key {key} value {value}")
                if len(self.squareposition[key]) > 0:
                    # print(key, value)
                    for i in value:
                        if i not in playerMoves:
                            squareformed = False
                            break
                    if squareformed:
                        # print(f"Player {player} formed square {min(value)}")  # .. delete the square from the dict
                        self.squareposition[key] = []
                        yield min(value)
                    else:
                        pass
                        # print(f"Player {player} not formed square")
                    squareformed = True
        yield -1

    def alignText(self, player, position, obj=None):
        font = pg.font.Font('freesansbold.ttf', 32)
        text = font.render(player, True, self.WHITE, self.BLACK)
        # print(f"position value {position}")
        pos = (
            self.pointpositiondict[self.linepositiondict[position][0]][0] + 20,
            self.pointpositiondict[self.linepositiondict[position][0]][1] + 10)
        # print(f"Text {player} position {pos}")
        if obj is None:
            self.screen.blit(text, pos)
        else:
            obj.screen.blit(text, pos)
        pg.display.update()

    def scorecalculation(self, result, player, obj=None):
        count = 0
        # print(f"result value is {result} and type is {type(result)}")
        for i in result:
            # print(f"generator value {i} and type {type(i)}")
            if i != -1:
                count += 1
                if player == "playera":
                    self.playerAScore += 1
                    self.alignText("A", i)
                else:
                    self.playerBScore += 1
                    self.alignText("B", i, obj)

        if count != 0:
            return True
        else:
            return False

    def nextMove(self):
        pg.display.update()
        if len(self.availableStates) != 0:
            move = -1
            print(f"Player {self.whoseMove} move {move}")
            if self.whoseMove == 0:
                move = random.choice(self.availableStates)
                self.visitedPositionNodes[move - 1] = 2
                self.playerAPosition.append(self.visitedPositionNodes.copy())
                print(f"{move} player A \t {self.visitedPositionNodes}")
                self.playerAmoves.append(move)
                self.visitedNodes.append(move)
                self.drawLine(move, color=self.WHITE)
                result = self.checkSquareFormed(self.visitedNodes, move, "PlayerA")
                self.whoseMove = 1
                if self.scorecalculation(result, "playera"):
                    self.whoseMove = 0
                    self.availableStates.remove(move)

            else:
                res = minimax.mainFunc(self.availableStates, self.visitedNodes, self, self.visitedPositionNodes,
                                       self.isGPUenabled)
                move = res[0]
                obj = res[1]
                # move = random.choice(self.availableStates)
                self.visitedPositionNodes[move - 1] = 1
                self.playerBPosition.append(self.visitedPositionNodes.copy())
                print(f"{move} player B \t {self.visitedPositionNodes}")
                print(f"minimax bestmove position is {move}")
                self.playerBmoves.append(move)
                self.visitedNodes.append(move)
                self.drawLine(move, color=(self.BLACK))
                result = self.checkSquareFormed(self.visitedNodes, move, "PlayerB")
                print(f"result {result}")
                self.whoseMove = 0
                if self.scorecalculation(result, "playerb", res[1]):
                    self.whoseMove = 1
                    self.availableStates.remove(move)
            pg.display.update()
            if move not in self.availableStates:
                return False
            self.availableStates.remove(move)
            return True
        return False

    def storetxt(self, playerAScore, playerBScore, playerAPosition, playerBPosition):
        print(f"PlayerA score {playerAScore} player B score {playerBScore}")
        if self.GRIDSIZE == 5:
            for i in playerAPosition:
                for j in i:
                    self.file.write(f"{j} \t")
                    # print(f"j {j} \t", end="")
                self.file.write(f"{playerAScore - playerBScore}")
                # print(f"{playerAScore - playerBScore} \t", end="")
                self.file.write("\n")
                # print("\n")

            for i in playerBPosition:
                for j in i:
                    self.file.write(f"{j} \t")
                    # print(f"j {j} \t", end="")
                self.file.write(f"{playerBScore - playerAScore}")
                # print(f"{playerAScore - playerBScore} \t", end="")
                self.file.write("\n")
                # print("\n")

        game_result = ""
        if playerAScore > playerBScore:
            print("PlayerA won the game")
            game_result = "PlayerA won the game"
        elif playerAScore == playerBScore:
            print("Tie")
            game_result = "Tie game"
        else:
            print("PlayerB won the game")
            game_result = "PlayerB won the game"

        font = pg.font.Font('freesansbold.ttf', 32)
        text = font.render(game_result, True, self.WHITE, self.BLACK)
        self.screen.blit(text, (400, 300))

        return playerAScore - playerBScore


if __name__ == "__main__":
    active = True
    singleexecution = True
    board = None
    gridSize = 5
    no_of_execution = 1
    isGPUenabled = False

    while active:
        if no_of_execution > 0:
            if singleexecution:
                board = Board(isGPUenabled, gridSize)
                board.intialize_board()
                board.drawGrid()
                board.constructLinePos()
                board.constructSquares()
                font = pg.font.Font('freesansbold.ttf', 18)
                text = f"PlayerA(White) is Random"
                font_text = font.render(text, True, board.WHITE, board.BLACK)
                board.screen.blit(font_text, (400, 100))
                text = f"PlayerB(Black) is AI"
                font_text = font.render(text, True, board.WHITE, board.BLACK)
                board.screen.blit(font_text, (400, 125))
                singleexecution = False

            if len(board.availableStates) != 0:
                board.nextMove()
            else:
                pg.time.wait(1000)
                board.storetxt(board.playerAScore, board.playerBScore, board.playerAPosition, board.playerBPosition)
                print("====================New Game======================")
                pg.time.wait(1000)
                no_of_execution -= 1
                singleexecution = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("Console Exited")
                active = False
                board.file.close()
        pg.display.update()
