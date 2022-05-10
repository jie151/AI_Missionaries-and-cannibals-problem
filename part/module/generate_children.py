from .node import Node
from .sortNode import sortNode
import numpy as np


def is_safe(totalM, totalC, right_m, right_c):
    m = right_m
    c = right_c
    leftM = totalM - m
    leftC = totalC - c
    if (m < c and m!= 0): # cannibals <= missionaries  unless missionaries == 0 (right bank)
        return False
    if (leftM < leftC) and leftM != 0: # cannibals <= missionaries  unless missionaries == 0 (left bank)
        return False
    if (m < 0 or c < 0 or leftM < 0 or leftC < 0): # the number of people cannot be less than 0
        return False
    if (m == 0 and leftM >= leftC): 
        return True
    if (leftM == 0 and m >= c):
        return True
    if m >= c and leftM >= leftC:
        return True

def get_all_children(curr_node, boatA_operations, boatB_operations, setting_state):
    successor = []
    right_m = curr_node.m
    right_c = curr_node.c
    totalM, totalC, costOrStep, bACost, bATime, bAMax, bBCost, bBTime, bBMax = setting_state
    left_m = totalM - right_m
    left_c = totalC - right_c  
   
    if (curr_node.bA > 0): # boat A on the right bank
        for boatA_operation in boatA_operations:
            bA_state = np.array([curr_node.bA, bACost, bATime, 1]) # 1: moving
            right_m_bA_to_left = right_m - boatA_operation[0] # 右岸剩下的傳教士 = 右岸原本的傳教士人數 - boatA載的傳教士人數
            right_c_bA_to_left = right_c - boatA_operation[1] # 右岸剩下的食人族 = 右岸原本的食人族人數 - boatA載的食人族人數

            if (boatA_operation[0] + boatA_operation[1] == 0):
                bA_state = [-curr_node.bA, 0, 0, 0] # bA_pos, bACost, bATime, bAmove
            if is_safe(totalM, totalC, right_m_bA_to_left, right_c_bA_to_left):

                if (curr_node.bB > 0): 
                # boat A : right bank, boat B: right bank
                    for boatB_operation in boatB_operations:
                        bB_state = np.array([curr_node.bB, bBCost, bBTime, 1]) # 1: moving

                        right_m_bB_to_left = right_m_bA_to_left -  boatB_operation[0] # 右岸剩下的傳教士 (右岸剩下的傳教士人數 - boatB載的傳教士人數)
                        right_c_bB_to_left = right_c_bA_to_left -  boatB_operation[1] # 右岸剩下的食人族 (右岸剩下的食人族人數 - boatB載的食人族人數)

                        if (boatB_operation[0] + boatB_operation[1] == 0):
                                bB_state = [-curr_node.bB, 0, 0, 0] # bB_pos, bBCost, bBTime, bBmove

                        if is_safe(totalM, totalC, right_m_bB_to_left, right_c_bB_to_left) and not(bA_state[3] == 0 and bB_state[3] == 0):
                            
                            step = curr_node.step + bA_state[2] + bB_state[2] - min(bA_state[2], bB_state[2]) #原本已經走的step加上boat A, boat B的step 減掉他們重疊的step
                            cost = curr_node.cost + bA_state[1] + bB_state[1]
                            successor.append(Node(right_m_bB_to_left, right_c_bB_to_left, -bA_state[0], bA_state[3], boatA_operation[0], boatA_operation[1], -bB_state[0], bB_state[3], boatB_operation[0], boatB_operation[1], step, cost, curr_node))
                else: 
                # boat A : right bank, boat B: left bank
                    for boatB_operation in boatB_operations:
                        bB_state = np.array([curr_node.bB, bBCost, bBTime, 1]) #1: moving
                        
                        left_m_bB_to_right_no = left_m - boatB_operation[0] # 左岸剩下的傳教士 (左岸原本的傳教士人數 - boatB載的傳教士人數)
                        left_c_bB_to_right_no = left_c - boatB_operation[1] # 左岸剩下的食人族 (左岸原本的食人族人數 - boatB載的食人族人數)
                        right_m_bB_to_right_no = right_m_bA_to_left + boatB_operation[0] # 右岸所有的傳教士 (右岸原本的傳教士人數 + boatB載的傳教士人數)
                        right_c_bB_to_right_no = right_c_bA_to_left + boatB_operation[1] # 右岸所有的食人族 (右岸原本的食人族人數 + boatB載的食人族人數)

                        if (boatB_operation[0] + boatB_operation[1] == 0):
                                bB_state = [-curr_node.bB, 0, 0, 0] #bB_pos, bBCost, bBTime, bBmove
                                
                        if is_safe(totalM, totalC, right_m_bB_to_right_no,  right_c_bB_to_right_no) and not(bA_state[3] == 0 and bB_state[3] == 0) and left_m_bB_to_right_no >= 0 and left_c_bB_to_right_no >= 0:
                            
                            step = curr_node.step + bA_state[2] + bB_state[2] - min(bA_state[2], bB_state[2]) #原本已經走的step加上boat A, boat B的step 減掉他們重疊的step
                            cost = curr_node.cost + bA_state[1] + bB_state[1]
                            successor.append(Node(right_m_bB_to_right_no,  right_c_bB_to_right_no, -bA_state[0], bA_state[3], boatA_operation[0], boatA_operation[1], -bB_state[0], bB_state[3], boatB_operation[0], boatB_operation[1], step, cost, curr_node))

    else : #boat A on the left bank
        for boatA_operation in boatA_operations:
            bA_state = np.array([curr_node.bA, bACost, bATime, 1]) #1: moving
            left_m_bA_to_right = left_m - boatA_operation[0] # 左岸剩下的傳教士 (左岸原本的傳教士人數 - boatA載的傳教士人數)
            left_c_bA_to_right = left_c - boatA_operation[1] # 左岸剩下的食人族 (左岸原本的食人族人數 - boatA載的食人族人數)
            right_m_bA_to_right = right_m + boatA_operation[0] # 右岸所有的傳教士 (右岸原本的傳教士人數 + boatA載的傳教士人數)
            right_c_bA_to_right = right_c + boatA_operation[1] # 右岸所有的食人族 (右岸原本的食人族人數 + boatA載的食人族人數)
            if (boatA_operation[0] + boatA_operation[1] == 0):
                bA_state = [-curr_node.bA, 0, 0, 0] # bA_pos, bACost, bATime, bAmove

            if is_safe(totalM, totalC, right_m_bA_to_right, right_c_bA_to_right) and left_m_bA_to_right + right_m_bA_to_right == totalM and left_c_bA_to_right + right_c_bA_to_right == totalC:
                
                if (curr_node.bB > 0): 
                # boat A : left bank, boat B: right bank
                    for boatB_operation in boatB_operations:
                        bB_state = np.array([curr_node.bB, bBCost, bBTime, 1]) #1: moving
                        
                        left_m_bB_to_left_no = left_m_bA_to_right + boatB_operation[0] # 左岸所有的傳教士 (左岸原本的傳教士人數 + boatB載的傳教士人數)
                        left_c_bB_to_left_no = left_c_bA_to_right + boatB_operation[1] # 左岸所有的食人族 (左岸原本的食人族人數 + boatB載的食人族人數)
                        right_m_bB_to_left_no = totalM - left_m_bB_to_left_no # 右岸剩下的傳教士 (右岸total會有的傳教士人數 - 左岸所有的傳教士) 避免算到A船載過去的人
                        right_c_bB_to_left_no = totalC - left_c_bB_to_left_no # 右岸剩下的食人族 (右岸total會有的食人族人數 - 左岸所有的食人族) 避免算到A船載過去的人

                        if (boatB_operation[0] + boatB_operation[1] == 0):
                                bB_state = [-curr_node.bB, 0, 0, 0] # bB_pos, bBCost, bBTime, bBmove
                                
                        if is_safe(totalM, totalC, right_m_bB_to_left_no,  right_c_bB_to_left_no) and not(bA_state[3] == 0 and bB_state[3] == 0) and right_m - boatB_operation[0] >= 0 and right_c - boatB_operation[1] >= 0 :
                            
                            step = curr_node.step + bA_state[2] + bB_state[2] - min(bA_state[2], bB_state[2]) # 原本已經走的step加上boat A, boat B的step 減掉他們重疊的step
                            cost = curr_node.cost + bA_state[1] + bB_state[1]
                            successor.append(Node(right_m_bB_to_left_no, right_c_bB_to_left_no, -bA_state[0], bA_state[3], boatA_operation[0], boatA_operation[1], -bB_state[0], bB_state[3], boatB_operation[0], boatB_operation[1], step, cost, curr_node))
                else: 
                # boat A : left bank, boat B: left bank
                    for boatB_operation in boatB_operations:
                        bB_state = np.array([curr_node.bB, bBCost, bBTime, 1]) #1: moving
            
                        right_m_bB_to_right = right_m_bA_to_right + boatB_operation[0] # 右岸所有的傳教士 (右岸原本的傳教士人數 + boatB載的傳教士人數)
                        right_c_bB_to_right = right_c_bA_to_right + boatB_operation[1] # 右岸所有的食人族 (右岸原本的食人族人數 + boatB載的食人族人數)

                        if (boatB_operation[0] + boatB_operation[1] == 0):
                                bB_state = [-curr_node.bB, 0, 0, 0] # bB_pos, bBCost, bBTime, bBmove
                                
                        if is_safe(totalM, totalC, right_m_bB_to_right, right_c_bB_to_right) and not(bA_state[3] == 0 and bB_state[3] == 0):
                            
                            step = curr_node.step + bA_state[2] + bB_state[2] - min(bA_state[2], bB_state[2]) # 原本已經走的step加上boat A, boat B的step 減掉他們重疊的step
                            cost = curr_node.cost + bA_state[1] + bB_state[1]
                            successor.append(Node(right_m_bB_to_right, right_c_bB_to_right, -bA_state[0], bA_state[3], boatA_operation[0], boatA_operation[1], -bB_state[0], bB_state[3], boatB_operation[0], boatB_operation[1], step, cost, curr_node))
    
    sortNode (successor, costOrStep)

    return successor