import numpy as np
import prettytable
import logging
import time

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

def boat_actions (id, boatSetting):
    set_boat_operation = []
    for i in range (boatSetting[id]['capacity'] + 1):
        if (i == 0): # 船上只有野人
            for j in range(0, boatSetting[id]['capacity'] + 1):
                set_boat_operation.append([i, j, boatSetting[id]['cost'], boatSetting[id]['step']])

        else: #船上有傳教士
            for j in range (0, i + 1):
                if i + j <= boatSetting[id]['capacity']:
                    set_boat_operation.append([i, j, boatSetting[id]['cost'], boatSetting[id]['step'] ])
    print(f"boat{id} 有{len(set_boat_operation)}種動作，各為:", set_boat_operation)
    return set_boat_operation

def sortNode (dataList, cost_or_step, useAStar):

    cost_or_step_or_aStar = 2 if useAStar else cost_or_step

    for i in range(len(dataList)):
        for j in range(i, len(dataList)):
            change = 0
            if (dataList[i].data[cost_or_step_or_aStar] < dataList[j].data[cost_or_step_or_aStar]):
                change = 1
            elif (dataList[i].data[cost_or_step_or_aStar] == dataList[j].data[cost_or_step_or_aStar]) and cost_or_step_or_aStar != 0: # 0 cost, 1 step, 2 aStar
                if (dataList[i].data[0] < dataList[j].data[0]):
                    change = 1
                elif (dataList[i].data[0] == dataList[j].data[0]) and dataList[i].data[2] < dataList[j].data[2]:
                    change = 1
            if change:
                temp = dataList[i]
                dataList[i] = dataList[j]
                dataList[j] = temp

def printNode(node, setting): # print node information
    print(f"right bank: m: {node.state['m']}, c: {node.state['c']}")
    print(f"left bank:  m: {setting['totalM'] - node.state['m']}, c: {setting['totalC'] - node.state['c']}")
    print(f"boat A: pos: {node.state['bA']}, move: {node.state['bAMove']}, m: {node.boatA['bA_m']}, c: {node.boatA['bA_c']}")
    print(f"boat B: pos: {node.state['bB']}, move: {node.state['bBMove']}, m: {node.boatB['bB_m']}, c: {node.boatB['bB_c']}")
    print(f"cost: {node.data[0]}, step: {node.data[1]}, h(n): {node.h}, f(n): {node.data[2]}\n")

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

def printTable(dataList, setting):
    table = prettytable.PrettyTable()
    table.field_names = ["step", "left m", "left c", "boatA direction", "boatA [m c]", "boatB direction", "boatB [m c]" , "right m", "right c", "cost", "AStar_h"]
    while dataList:
        node = dataList.pop()
        if (node.state['bA'] == -1 and node.state['bAMove'] == 1):
            boatA_direction = "L <- R"
        elif(node.state['bA'] == -1 and node.state['bAMove'] == 0):
            boatA_direction = "L (X)"
        elif (node.state['bA'] == 1 and node.state['bAMove'] == 1):
            boatA_direction = "L -> R"
        else :
            boatA_direction = "R (X)"

        if (node.state['bB'] == -1 and node.state['bBMove'] == 1):
            boatB_direction = "L <- R"
        elif(node.state['bB'] == -1 and node.state['bBMove'] == 0):
            boatB_direction = "L (X)"
        elif (node.state['bB'] == 1 and node.state['bBMove'] == 1):
            boatB_direction = "L -> R"
        else :
            boatB_direction = "R (X)"

        table.add_row([ node.data[1], setting['totalM'] - node.state['m'], setting['totalC'] - node.state['c'],
                        boatA_direction, list(node.boatA.values()), boatB_direction, list(node.boatB.values()),
                        node.state['m'], node.state['c'], node.data[0], node.h])
    print(table)

logging.basicConfig(filename='aStar_new.log', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')
def logging_file(open_list, close_list):
    logging.info('********open list********, len = {}'.format(len(open_list)))
    for open_data in open_list:
        logging.debug('{}\n> cost = {}, step = {}, f(n) = {}\n> {}\n> {}'.format(   open_data.state,
                                                                                    open_data.data[0], open_data.data[1], open_data.data[2],
                                                                                    open_data.boatA, open_data.boatB))
    logging.info('********close list********, len = {}'.format(len(close_list)))
    for close_data in close_list:
        logging.debug('{}\n> cost = {}, step = {}, f(n) = {}\n> {}\n> {}'.format(   close_data.state,
                                                                                    close_data.data[0], close_data.data[1], close_data.data[2],
                                                                                    close_data.boatA, close_data.boatB))
    logging.info('--------------------------------------------------------------------------------------------------------')

def calculate_path(curr_node):
    result = []
    result.append(curr_node)
    parent_node = curr_node.parent
    while (parent_node):
        result.append(parent_node)
        parent_node = parent_node.parent
    return result

def uniform_cost_search(goal, start_node, setting, boatSetting):
    open_list = []
    close_list = []
    open_list.append(start_node)
    useAStar = 0

    while True:
        if not open_list:
            print ("no solution!!!")
            break

        curr_node = open_list.pop()

        if (curr_node.state['m'] == goal[0] and curr_node.state['c'] == goal[1] ):
            result = calculate_path(curr_node)
            print("****************")
            printTable(result, setting)
            break

        close_list.append(curr_node)
        children = get_all_children(curr_node, boatA_operations, boatB_operations, setting, boatSetting, useAStar) # cost: 0 , time: 1

        for child in children:
            sameNode_in_open_list = 0
            sameNode_in_close_list = 0

            for i in range(len(close_list)):
                if np.array_equal(child.state, close_list[i].state): #and np.array_equal(child.data, close_list[i].data):
                    sameNode_in_close_list = 1
                    break

            for j in range(len(open_list)):
                if np.array_equal(child.state, open_list[j].state):
                    sameNode_in_open_list = 1
                    if child.data[ setting['costOrStep'] ] < open_list[j].data[ setting['costOrStep'] ]:
                        open_list.pop(j)
                    break

            if (sameNode_in_close_list != 1 and sameNode_in_open_list != 1):
                open_list.append(child)
        sortNode(open_list, setting['costOrStep'], useAStar)
        logging_file(open_list, close_list)

def AStart_algorithm(goal, start_node, setting, boatSetting):
    open_list = []
    close_list = []
    open_list.append(start_node)
    useAStar = 1

    while True:
        if not open_list:
            print ("no solution!!!")
            break

        curr_node = open_list.pop()

        if (curr_node.state['m'] == goal[0] and curr_node.state['c'] == goal[1] ):
            result = calculate_path(curr_node)
            print("****************")
            printTable(result, setting)
            break

        close_list.append(curr_node)
        children = get_all_children(curr_node, boatA_operations, boatB_operations, setting, boatSetting, useAStar)

        for child in children:
            sameNode_in_open_list = 0
            sameNode_in_close_list = 0

            for i in range(len(open_list)):
                if np.array_equal(child.state, open_list[i].state):
                    if child.data[2] < open_list[i].data[2]: # beter => remove older, append newer, AStar_f
                        open_list.pop(i)
                    else : # newer no better
                        sameNode_in_open_list = 1
                    break

            if (sameNode_in_open_list != 1):
                for j in range(len(close_list)):
                    if np.array_equal(child.state, close_list[j].state):
                        if child.data[2] < close_list[j].data[2]: # beter => remove older, append newer, AStar_f
                            close_list.pop(j)
                        else : # newer no better
                            sameNode_in_close_list = 1
                        break

                if (sameNode_in_close_list != 1):
                    open_list.append(child)
        sortNode(open_list, setting['costOrStep'], useAStar)
        logging_file(open_list, close_list)


boatSetting = dict()
boatSetting['A'] = { 'capacity': 2, 'cost': 3,  'step' : 1, 'pos' : 1} # pos : right bank: 1, left bank: -1
boatSetting['B'] = { 'capacity': 3, 'cost': 25, 'step' : 1, 'pos' : 1}
setting = {'totalM': 7, 'totalC' : 7, 'costOrStep' : 1}

boatA_operations = boat_actions('A', boatSetting)
boatB_operations = boat_actions('B', boatSetting)

#start_node = Node(setting['totalM'], setting['totalC'], 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, None, setting, boatSetting) # 初始狀態節點
#goal_node = [0, 0]
#uniform_cost_search(goal_node, start_node, setting, boatSetting)
#AStart_algorithm(goal_node, start_node, setting, boatSetting)

for m in range(3):
    for n in range (3, 11):
        if m + n == n and n > 6:
            break
        setting = {'totalM': m+n, 'totalC' : n, 'costOrStep' : 1}
        print(m+n, n)
        start_node = Node(m + n, n, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, None, setting, boatSetting) # 初始狀態節點
        goal_node = [0, 0]
        AStart_algorithm (goal_node, start_node, setting, boatSetting)
        uniform_cost_search(goal_node, start_node, setting, boatSetting)
