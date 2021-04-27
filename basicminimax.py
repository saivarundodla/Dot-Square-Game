import main
import numpy as np
import neuralnetwork as nn

playerAScore = 0
playerBScore = 0

playerAmoves = []
playerBmoves = []

board = main.Board()

board.constructSquares()


def minimax(playerAmoves=[], playerBmoves=[], length=0, limit=6, isMaximizing=True, alpha=0, beta=0):
    global playerAScore
    global playerBScore
    if length == limit or length == 0:
        # print(f"{playerAmoves} {playerBmoves}  playerAScore {playerAScore}  playerBScore {playerBScore}\n")
        result = playerAScore - playerBScore
        visitedPositionNodes = visitedPositionNode.copy()
        playerAScore = 0
        playerBScore = 0
        playerAlen = len(playerAmoves)
        playerBlen = len(playerBmoves)
        playerlen = 0
        if playerAlen > playerBlen:
            playerlen = playerAlen
        else:
            playerlen = playerBlen

        for i in range(playerlen):
            if i < playerAlen:
                visitedPositionNodes[playerAmoves[i] - 1] = -1
            if i < playerBlen:
                visitedPositionNodes[playerBmoves[i] - 1] = 1
        nn_result = None
        if isGPUEnabled:
            nn_result = nn.predict_model(visitedPositionNodes.reshape(1, visitedPositionNodelen))
        board.constructSquares()
        if isGPUEnabled and result < nn_result:
            return int(np.round(nn_result,0))
        return result

    if isMaximizing:
        bestscore = -100
        length -= 1
        # print("Maximizing Player")
        for i in availablestates:
            # print(f"i value is {i} and l {l}")
            if i not in playerAmoves + playerBmoves:
                playerAmoves.append(i)
                count = 0
                # print(f"Maximizing Before Available list {playerAmoves}")
                for j in board.checkSquareFormed(visitednodes + playerAmoves + playerBmoves, player='PlayerA'):
                    if j != -1:
                        count += 1
                if count != 0:
                    playerAScore += count
                    # print(f"Square Formed Extra turn for the player A {playerAScore} {count}")
                score = minimax(playerAmoves, playerBmoves, length, limit, False, alpha, beta)
                playerAmoves.remove(i)
                bestscore = max(bestscore, score)
                alpha = max(alpha, bestscore)
                if beta <= alpha:
                    break
                # print(f"Maximizing After Available list {playerAmoves}")
        return bestscore
    else:
        bestscore = 100
        length -= 1
        # print("Minimizing Player")
        for i in availablestates:
            # print(f"i value is {i} and l {l}")
            if i not in playerAmoves + playerBmoves:
                playerBmoves.append(i)
                count = 0
                # print(f"Minimizing Player Before Available list {playerBmoves}")
                for j in board.checkSquareFormed(visitednodes + playerAmoves + playerBmoves, player='PlayerB'):
                    if j != -1:
                        count += 1
                if count != 0:
                    playerBScore += count
                    # print(f"Square Formed Extra turn for the player B {playerBScore}")
                score = minimax(playerAmoves, playerBmoves, length, limit, True, alpha, beta)
                playerBmoves.remove(i)
                bestscore = min(bestscore, score)
                beta = min(beta, bestscore)
                if beta <= alpha:
                    break
        return bestscore


def mainFunc(possiblemoves, visitednode, obj, visitedPositionNodes, isGPUenabled):
    global availablestates
    global visitednodes
    global visitedPositionNode
    global visitedPositionNodelen
    global isGPUEnabled

    availablestates = possiblemoves
    visitednodes = visitednode
    visitedPositionNode = np.array(visitedPositionNodes, dtype="int32")
    visitedPositionNodelen = len(visitedPositionNode)
    isGPUEnabled = isGPUenabled

    bestmove = 0
    previousfinalscore = -100
    limit = len(availablestates) - 5
    if isGPUenabled:
        limit = len(availablestates) - 2
    for i in availablestates:
        final_score = minimax([i], [], len(availablestates) - 1, limit, False, float('-inf'), float('inf'))
        if previousfinalscore < final_score:
            previousfinalscore = final_score
            bestmove = i

    if bestmove == 0:
        bestmove = availablestates[0]
    return (bestmove, obj)
