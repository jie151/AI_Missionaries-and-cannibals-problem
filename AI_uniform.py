import queue
import numpy as np
import prettytable
import logging 

totalM = int(input("請輸入傳教士的人數: ")) # total Missionaries (right bank)  
totalC = int(input("請輸入野人的人數: "))  # total cannibals (right bank) 
while totalM < totalC:
    totalM = int(input("請再次輸入傳教士的人數: ")) # total Missionaries (right bank)  
    totalC = int(input("請再次輸入野人的人數: "))  # total cannibals (right bank) 

costOrStep = int(input("cost輸入0, step輸入1: "))
bAMax = 2 # Boat A maximum capacities: 2 persons
bBMax = 3 # Boat B maximum capacities: 3 persons
bACost = 3  # fare
bBCost = 25 # fare
bATime = 1
bBTime = 1 
bAPos = 1 # right bank: 1, left bank: -1
bBPos = 1 # right bank: 1, left bank: -1
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

def is_safe(right_m, right_c):
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

def boatA_actions (bAMax, bAcost, bAtime):
    set_boatA_operation = [] 
    for i in range (bAMax + 1):
        if (i == 0): # 船上只有野人
            for j in range(0, bAMax + 1):  
                set_boatA_operation.append([i, j, bAcost, bAtime])
        else: #船上有傳教士
            for j in range (0, i + 1):
                if i + j <= bAMax: 
                    set_boatA_operation.append([i, j, bAcost, bAtime]) 
    print("boatA所有動作為: ", set_boatA_operation)
    return set_boatA_operation

def boatB_actions (bBMax, bBcost, bBtime):
    set_boatB_operation = [] 
    for i in range (bBMax + 1):
        if (i == 0): #船上只有野人
            for j in range(0, bBMax + 1):
                set_boatB_operation.append([i, j, bBcost, bBtime])
        else: #船上有傳教士
            for j in range (0, i + 1):
                if i + j <= bBMax:
                    set_boatB_operation.append([i, j, bBcost, bBtime])
    print("boatB所有動作為: ", set_boatB_operation)
    return set_boatB_operation

boatA_operations = boatA_actions(2, bACost, bATime)
boatB_operations = boatB_actions(3, bBCost, bBTime)

def sortNode (dataList, cost_or_time):
    for i in range(len(dataList)):
        for j in range(i, len(dataList)):
            if (dataList[i].data[cost_or_time] < dataList[j].data[cost_or_time]):
                temp = dataList[i]
                dataList[i] = dataList[j]
                dataList[j] = temp  
def printNode(node): # print node information
    print(f"right bank: m: {node.m}, c: {node.c}")
    print(f"left bank:  m: {totalM - node.m}, c: {totalC - node.c}")
    print(f"boat A: pos: {node.bA}, move: {node.bAMove}, m: {node.bA_m}, c: {node.bA_c}")
    print(f"boat B: pos: {node.bB}, move: {node.bBMove}, m: {node.bB_m}, c: {node.bB_c}")
    print(f"cost: {node.cost}, step: {node.step}\n")

def get_all_children(curr_node, boatA_operations, boatB_operations):
    successor = []
    right_m = curr_node.m
    right_c = curr_node.c
    left_m = totalM - right_m
    left_c = totalC - right_c  
   
    if (curr_node.bA > 0): # boat A on the right bank
        for boatA_operation in boatA_operations:
            bA_state = np.array([curr_node.bA, bACost, bATime, 1]) # 1: moving
            right_m_bA_to_left = right_m - boatA_operation[0] # 右岸剩下的傳教士 = 右岸原本的傳教士人數 - boatA載的傳教士人數
            right_c_bA_to_left = right_c - boatA_operation[1] # 右岸剩下的食人族 = 右岸原本的食人族人數 - boatA載的食人族人數

            if (boatA_operation[0] + boatA_operation[1] == 0):
                bA_state = [-curr_node.bA, 0, 0, 0] # bA_pos, bACost, bATime, bAmove
            if is_safe(right_m_bA_to_left, right_c_bA_to_left):

                if (curr_node.bB > 0): 
                # boat A : right bank, boat B: right bank
                    for boatB_operation in boatB_operations:
                        bB_state = np.array([curr_node.bB, bBCost, bBTime, 1]) # 1: moving

                        right_m_bB_to_left = right_m_bA_to_left -  boatB_operation[0] # 右岸剩下的傳教士 (右岸剩下的傳教士人數 - boatB載的傳教士人數)
                        right_c_bB_to_left = right_c_bA_to_left -  boatB_operation[1] # 右岸剩下的食人族 (右岸剩下的食人族人數 - boatB載的食人族人數)

                        if (boatB_operation[0] + boatB_operation[1] == 0):
                                bB_state = [-curr_node.bB, 0, 0, 0] # bB_pos, bBCost, bBTime, bBmove

                        if is_safe(right_m_bB_to_left, right_c_bB_to_left) and not(bA_state[3] == 0 and bB_state[3] == 0):
                            
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
                                
                        if is_safe( right_m_bB_to_right_no,  right_c_bB_to_right_no) and not(bA_state[3] == 0 and bB_state[3] == 0) and left_m_bB_to_right_no >= 0 and left_c_bB_to_right_no >= 0:
                            
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

            if is_safe(right_m_bA_to_right, right_c_bA_to_right) and left_m_bA_to_right + right_m_bA_to_right == totalM and left_c_bA_to_right + right_c_bA_to_right == totalC:
                
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
                                
                        if is_safe(right_m_bB_to_left_no,  right_c_bB_to_left_no) and not(bA_state[3] == 0 and bB_state[3] == 0) and right_m - boatB_operation[0] >= 0 and right_c - boatB_operation[1] >= 0 :
                            
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
                                
                        if is_safe(right_m_bB_to_right, right_c_bB_to_right) and not(bA_state[3] == 0 and bB_state[3] == 0):
                            
                            step = curr_node.step + bA_state[2] + bB_state[2] - min(bA_state[2], bB_state[2]) # 原本已經走的step加上boat A, boat B的step 減掉他們重疊的step
                            cost = curr_node.cost + bA_state[1] + bB_state[1]
                            successor.append(Node(right_m_bB_to_right, right_c_bB_to_right, -bA_state[0], bA_state[3], boatA_operation[0], boatA_operation[1], -bB_state[0], bB_state[3], boatB_operation[0], boatB_operation[1], step, cost, curr_node))
    
    sortNode (successor, costOrStep)

    return successor

def printTable(dataList):
    table = prettytable.PrettyTable()
    table.field_names = ["step", "left m", "left c", "boatA direction", "boatA [m c]", "boatB direction", "boatB [m c]" , "right m", "right c", "cost"]
    while dataList:
        node = dataList.pop()
        if (node.bA == -1 and node.bAMove == 1):
            boatA_direction = "L <- R"
        elif(node.bA == -1 and node.bAMove == 0):
            boatA_direction = "left (X)"
        elif (node.bA == 1 and node.bAMove == 1):
            boatA_direction = "L -> R"
        else :
            boatA_direction = "right (X)"

        if (node.bB == -1 and node.bBMove == 1):
            boatB_direction = "L <- R"
        elif(node.bB == -1 and node.bBMove == 0):
            boatB_direction = "left (X)"
        elif (node.bB == 1 and node.bBMove == 1):
            boatB_direction = "L -> R"
        else :
            boatB_direction = "right (X)"

        table.add_row([node.step, totalM - node.m, totalC - node.c,boatA_direction, node.boatA, boatB_direction, node.boatB, node.m, node.c, node.cost])
    print(table)

def calculate_path(curr_node):
    result = []
    result.append(curr_node)
    parent_node = curr_node.parent
    while (parent_node):
        result.append(parent_node)
        parent_node = parent_node.parent
    return result

logging.basicConfig(filename='UCS.log', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')

def logging_file(open_list, close_list):
    logging.info('********open list********')
    for open_data in open_list:
        logging.debug('[rightM, rightC] = {}\n> boatA[pos, move, m, c] = {} {}\n> boatB[pos, move, m, c] = {} {}'.format(open_data.state[:2], open_data.state[2:4], open_data.boatA, open_data.state[4:], open_data.boatB))
    logging.info('********close list********')
    for close_data in close_list:
        logging.debug('[rightM, rightC] = {}\n> boatA[pos, move, m, c] = {} {}\n> boatB[pos, move, m, c] = {} {}'.format(close_data.state[:2], close_data.state[2:4], close_data.boatA, close_data.state[4:], close_data.boatB))
    logging.info('--------------------------------------------------------------------------------------------------------')
        
def uniform_cost_search(goal, start_node):
    
    priority_queue = queue.PriorityQueue()
    priority_queue.put((start_node.data[costOrStep] , start_node))
    open_list = []
    close_list = []
    open_list.append(start_node)
    
    while True:
        
        if not open_list:
            print ("no solution!!!")
            break
        
        curr_node = open_list.pop()

        if (curr_node.m == goal[0] and curr_node.c == goal[1] ):
            result = calculate_path(curr_node)
            print("****************")
            printTable(result)
            break

        close_list.append(curr_node)
        children = get_all_children(curr_node, boatA_operations, boatB_operations) # cost: 0 , time: 1
        
        for child in children:
            sameNode_in_open_list = 0
            sameNode_in_close_list = 0
            for i in range(len(close_list)):
                if np.array_equal(child.state, close_list[i].state) and np.array_equal(child.data, close_list[i].data):
                    sameNode_in_close_list = 1
                    break
                
            for j in range(len(open_list)):
                if np.array_equal(child.state, open_list[j].state):
                    sameNode_in_open_list = 1
                    if child.data[costOrStep] < open_list[j].data[costOrStep]:
                        open_list.pop(j)
                        open_list.append(i)
                    break
            
            if (sameNode_in_close_list != 1 and sameNode_in_open_list != 1):
                open_list.append(child)
        sortNode(open_list, costOrStep)
        logging_file(open_list, close_list)
        
start_node = Node(totalM, totalC, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, None) # 初始狀態節點
goal_node = [0, 0]
#get_all_children(start_node, boatA_operations, boatB_operations)
uniform_cost_search(goal_node, start_node)