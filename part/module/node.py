import numpy as np
class Node:
    def __init__(self, m, c, bA_pos, bA_move, bA_m, bA_c, bB_pos, bB_move, bB_m, bB_c, step, cost, parent, setting, boatSetting):
        self.state = {  'm' : m, 'c' : c,
                        'bA' : bA_pos, 'bAMove' : bA_move, # bA_pos: boat A's position，right : 1 (right -> left), left:-1 (left -> right)
                        'bB' : bB_pos, 'bBMove' : bB_move } # moving : 1

        self.boatA = {'bA_m' : bA_m, 'bA_c' : bA_c} # Missionaries on boat A, cannibals on boat A
        self.boatB = {'bB_m' : bB_m, 'bB_c' : bB_c} # Missionaries on boat B, cannibals on boat B

        h = m  + c  - bA_pos * boatSetting['A']['capacity'] * bA_move - bB_pos * boatSetting['B']['capacity'] * bB_move
        if h < 0 or m + c == 0:
            h = 0
        self.h = h
        f = h + step if setting['costOrStep'] else h + cost
        self.data = np.array([cost, step, f])
        # cost: total cost, step: number of steps
        self.parent = parent