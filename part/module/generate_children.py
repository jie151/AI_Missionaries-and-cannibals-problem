from .node import Node
from .sortNode import sortNode
import numpy as np

def is_safe(right_m, right_c, left_m, left_c, setting):
    m = right_m
    c = right_c
    total_m = right_m + left_m
    total_c = right_c + left_c

    if m < 0 or c < 0 or left_m < 0 or left_c < 0 or total_m != setting['totalM'] or total_c != setting['totalC']:
        # the number of people cannot be less than 0
        return False

    if m == total_m and c == total_c:
        return False

    if (m < c and m!= 0) or ( (left_m < left_c) and left_m != 0):
        # cannibals <= missionaries  unless missionaries == 0 (right/left bank)
        return False

    if (m == 0 and left_m >= left_c) or (left_m == 0 and m >= c) or (m >= c and left_m >= left_c):
        return True

def get_all_children(curr_node, boatA_operations, boatB_operations, setting, boatSetting, useAStar):
    successor = []
    right_m = curr_node.state['m']
    right_c = curr_node.state['c']
    left_m = setting['totalM'] - right_m
    left_c = setting['totalC'] - right_c

    for boatA_operation in boatA_operations:

        if (boatA_operation[0] + boatA_operation[1] != 0):
            bA_state = np.array([curr_node.state['bA'], boatSetting['A']['cost'], boatSetting['A']['step'], 1]) # 1: moving
        else:
            bA_state = [-curr_node.state['bA'], 0, 0, 0] # bA_pos, bACost, bATime, bAmove

        if curr_node.state['bA'] > 0:
            # boat A on the right bank
            boatA_m_to_left = boatA_operation[0]
            boatA_c_to_left = boatA_operation[1]
        else:
            # boat A on the left bank
            boatA_m_to_left = -boatA_operation[0]
            boatA_c_to_left = -boatA_operation[1]

        right_m_bA = right_m - boatA_m_to_left # 右岸剩下的傳教士 = 右岸原本的傳教士人數 -/+ boatA載的傳教士人數
        right_c_bA = right_c - boatA_c_to_left # 右岸剩下的食人族 = 右岸原本的食人族人數 -/+ boatA載的食人族人數
        left_m_bA = left_m + boatA_m_to_left # 左岸剩下的傳教士 (左岸原本的傳教士人數 +/- boatA載的傳教士人數)
        left_c_bA = left_c + boatA_c_to_left # 左岸剩下的食人族 (左岸原本的食人族人數 +/- boatA載的食人族人數)

        if not is_safe(right_m_bA, right_c_bA, left_m_bA, left_c_bA, setting):
            continue

        for boatB_operation in boatB_operations:

            if (boatB_operation[0] + boatB_operation[1] != 0):
                bB_state = np.array([curr_node.state['bB'], boatSetting['B']['cost'], boatSetting['B']['step'], 1]) # 1: moving
            else :
                bB_state = [-curr_node.state['bB'], 0, 0, 0] # bB_pos, bBCost, bBTime, bBmove

            if curr_node.state['bB'] > 0:
            # boat B on the right bank
                boatB_m_to_left = boatB_operation[0]
                boatB_c_to_left = boatB_operation[1]
            else:
                # boat B on the left bank
                boatB_m_to_left = -boatB_operation[0]
                boatB_c_to_left = -boatB_operation[1]

            right_m_bB = right_m_bA - boatB_m_to_left # 右岸剩下的傳教士 (右岸剩下的傳教士人數 -/+ boatB載的傳教士人數)
            right_c_bB = right_c_bA - boatB_c_to_left # 右岸剩下的食人族 (右岸剩下的食人族人數 -/+ boatB載的食人族人數)
            left_m_bB = left_m_bA + boatB_m_to_left # 左岸剩下的傳教士 (左岸原本的傳教士人數 +/- boatB載的傳教士人數)
            left_c_bB = left_c_bA + boatB_c_to_left # 左岸剩下的食人族 (左岸原本的食人族人數 +/- boatB載的食人族人數)

            if is_safe(right_m_bB, right_c_bB, left_m_bB, left_c_bB, setting) and not(bA_state[3] == 0 and bB_state[3] == 0):

                step = curr_node.data[1] + bA_state[2] + bB_state[2] - min(bA_state[2], bB_state[2]) #原本已經走的step加上boat A, boat B的step 減掉他們重疊的step
                cost = curr_node.data[0] + bA_state[1] + bB_state[1]
                successor.append(Node(right_m_bB, right_c_bB, -bA_state[0], bA_state[3], boatA_operation[0], boatA_operation[1], -bB_state[0], bB_state[3], boatB_operation[0], boatB_operation[1], step, cost, curr_node, setting, boatSetting))

    sortNode (successor, setting['costOrStep'], useAStar)
    #for node in successor:
    #    printNode(node, setting)
    return successor
