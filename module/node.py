import numpy as np
class Node:
    def __init__(self, m, c, bA_pos, bA_move, bA_m, bA_c, bB_pos, bB_move, bB_m, bB_c, step, cost, parent):
        self.state = np.array([m, c, bA_pos, bA_move, bB_pos, bB_move])
        self.data = np.array([cost, step])
        self.boatA = np.array([bA_m, bA_c])
        self.boatB = np.array([bB_m, bB_c])
        self.m = m    # m:the number of Missionaries  (right bank)  
        self.c = c    # c:the number of cannibals  (right bank)  
        self.bA_m = bA_m # Missionaries on boat A
        self.bA_c = bA_c # cannibals on boat A
        self.bB_m = bB_m # Missionaries on boat B
        self.bB_c = bB_c # cannibals on boat B
        self.bA = bA_pos  # bA: boat A's position，right : 1 (right -> left), left:0 (left -> right)
        self.bB = bB_pos  # bB: boat B's position，right : 1 (right -> left), left:0 (left -> right)
        self.bAMove = bA_move # moving: 1
        self.bBMove = bB_move # moving: 1
        self.step = step # number of steps
        self.cost = cost # total cost
        #self.h = m + c - Ka * ba * ba_move - Kb * bB * bb_move # heuristic function
        self.parent = parent