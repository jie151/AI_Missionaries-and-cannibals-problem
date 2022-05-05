import queue
import numpy as np
import prettytable as pt

# rightM = int(input("請輸入傳教士的人數: ")) #右岸的傳教士要送到左岸
# rightC = int(input("請輸入食人族的人數: "))  # 右岸的食人族要送到左岸
totalM = 3 #右岸的傳教士人數
totalC = 3 #左岸的傳教士人數
bAMax = 2 #boat a 最多可載2人
bBMax = 3 #boat b 最多可載3人
bACost = 3  #一趟的花費
bBCost = 25 #一趟的花費
bATime = 1
bBTime = 1 
bAPos = 1 #初始在右岸
bBPos = 1 #初始在右岸 
costOrTime = 0 #cost:0, time:1

class Node:
    def __init__(self, m, c, bA_pos, bA_move, bA_m, bA_c, bB_pos, bB_move, bB_m, bB_c, step, cost, parent):
        self.m = m    # m:右岸的傳教士数量
        self.c = c    # c:右岸食人族数量
        self.bA_m = bA_m #boat A 傳教士的人數
        self.bA_c = bA_c #boat A 食人族的人數
        self.bB_m = bB_m #boat B 傳教士的人數
        self.bB_c = bB_c #obat B 食人族的人數
        self.bA = bA_pos  # bA:船的位置，右岸: 1 (右 -> 左), 左岸:0 (左 -> 右)
        self.bB = bB_pos  # bB:船的位置，右岸: 1, 左岸:0
        self.bAMove = bA_move # moving: 1
        self.bBMove = bB_move # moving: 1
        self.step = step # step數
        self.cost = cost # 成本
        #self.h = m + c - Ka * ba * ba_move - Kb * bB * bb_move #評估值
        self.parent = parent
    
def printNode(node): #print()
    print(f"right bank: m: {node.m}, c: {node.c}")
    print(f"left bank:  m: {totalM - node.m}, c: {totalC - node.c}")
    print(f"boat A: pos: {node.bA}, move: {node.bAMove}, m: {node.bA_m}, c: {node.bA_c}")
    print(f"boat B: pos: {node.bB}, move: {node.bBMove}, m: {node.bB_m}, c: {node.bB_c}")
    print(f"cost: {node.cost}, step: {node.step}")


# right side m and c
def is_safe(right_m, right_c):
    m = right_m
    c = right_c
    leftM = totalM - m
    leftC = totalC - c
    if (m < c and m!= 0): #右岸食人族人數不能大於傳教士，除非傳教士為0
        return False
    if (leftM < leftC) and m != totalM: #左岸的食人族人數不能大於傳教士，除非左岸傳教士為0
        return False
    if (m < 0 or c < 0): #人數不能小於0
        return False
    if (m == 0 and leftM >= leftC):
        return True
    if (leftM == 0 and m >= c):
        return True
    if m >= c and leftM >= leftC:
        return True

def boatA_actions (bAMax, bAcost, bAtime):
    set_boatA_operation = [] 
    # A's all actions, table on excel
    for i in range (bAMax + 1):
        if (i == 0): #船上只有食人族
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
    # B's all actions, table on excel
    for i in range (bBMax + 1):
        if (i == 0): #船上只有食人族
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


def get_all_children(curr_node, cost_or_time, boatA_operations, boatB_operations):
    successor = []
    right_m = curr_node.m
    right_c = curr_node.c
    left_m = totalM - right_m
    left_c = totalC - right_c  

    # if boat A at right side
    # boat_operations([m, c, cost, time])
    if (curr_node.bA>0): 
        for boatA_operation in boatA_operations:
            # bA_state([position, cost, time, move or not])
            bA_state = np.array([curr_node.bA, bACost, bATime, 1]) #1: moving
            right_m_bA = right_m - boatA_operation[0] #right_m_bA右岸剩下的傳教士 (右岸原本的傳教士人數 - boatA載的傳教士人數)
            right_c_bA = right_c - boatA_operation[1] #right_c_bA右岸剩下的食人族 (右岸原本的食人族人數 - boatA載的食人族人數)
            if (boatA_operation[0] + boatA_operation[1] == 0):
                bA_state = [-curr_node.bA, 0, 0, 0] #bA_pos, bACost, bATime, bAmove
            if is_safe(right_m_bA, right_c_bA):
                if (curr_node.bB>0):
                    for boatB_operation in boatB_operations:
                        bB_state = np.array([curr_node.bB, bBCost, bBTime, 1]) #1: moving
                        right_m_bB = right_m_bA -  boatB_operation[0] #right_m_bB右岸剩下的傳教士 (右岸剩下的傳教士人數 - boatB載的傳教士人數)
                        right_c_bB = right_c_bA -  boatB_operation[1] #right_c_bB右岸剩下的食人族 (右岸剩下的食人族人數 - boatB載的食人族人數)
                        if (boatB_operation[0] + boatB_operation[1] == 0):
                                bB_state = [-curr_node.bB, 0, 0, 0] #bB_pos, bBCost, bBTime, bBmove

                        # safe and move 1 or 2 boat 
                        if is_safe(right_m_bB, right_c_bB) and not(bA_state[3] == 0 and bB_state[3] == 0):
                            
                            step = curr_node.step + bA_state[2] + bB_state[2] - min(bA_state[2], bB_state[2]) #原本已經走的step加上boat A, boat B的step 減掉他們重疊的step
                            cost = curr_node.cost + bA_state[1] + bB_state[1]
                            successor.append(Node(right_m_bB, right_c_bB, -bA_state[0], bA_state[3], boatA_operation[0], boatA_operation[1], -bB_state[0], bB_state[3], boatB_operation[0], boatB_operation[1], step, cost, curr_node))
                            print(f"boatA: m {boatA_operation[0]}, c {boatA_operation[1]}")
                            print(f"boatB: m {boatB_operation[0]}, c {boatB_operation[1]}")
                            print(f"右傳 {right_m_bB}, 食 {right_c_bB}, 左傳 {totalM - right_m_bB}, 食 {totalC - right_c_bB}")
                            print(f"cost: {cost}, step: {step}\n")

                else: #boat B on the left bank
                    for boatB_operation in boatB_operations:
                        bB_state = np.array([curr_node.bB, bBCost, bBTime, 1]) #1: moving
                        
                        left_m_bB = left_m - boatB_operation[0] #left_m_bB左岸剩下的傳教士 (左岸原本的傳教士人數 - boatA載的傳教士人數)
                        left_c_bB = left_c - boatB_operation[1] #left_c_bB左岸剩下的食人族 (左岸原本的食人族人數 - boatB載的食人族人數)
                        left_m_bB_right = right_m_bA + boatB_operation[0] #right_m_bB右岸所有的傳教士 (右岸原本的傳教士人數 + boatB載的傳教士人數)
                        left_c_bB_right = right_c_bA + boatB_operation[1] #right_c_bB右岸所有的食人族 (右岸原本的食人族人數 + boatB載的食人族人數)

                        if (boatB_operation[0] + boatB_operation[1] == 0):
                                bB_state = [-curr_node.bB, 0, 0, 0] #bB_pos, bBCost, bBTime, bBmove
                                
                        if is_safe( left_m_bB_right,  left_c_bB_right) and not(bA_state[3] == 0 and bB_state[3] == 0) and left_m_bB >= 0 and left_c_bB >= 0:
                            
                            step = curr_node.step + bA_state[2] + bB_state[2] - min(bA_state[2], bB_state[2]) #原本已經走的step加上boat A, boat B的step 減掉他們重疊的step
                            cost = curr_node.cost + bA_state[1] + bB_state[1]
                            successor.append(Node(left_m_bB_right, left_c_bB_right, -bA_state[0], bA_state[3], boatA_operation[0], boatA_operation[1], -bB_state[0], bB_state[3], boatB_operation[0], boatB_operation[1], step, cost, curr_node))
                            #print(f"boatA: m {boatA_operation[0]}, c {boatA_operation[1]}")
                            #print(f"boatB: m {boatB_operation[0]}, c {boatB_operation[1]}")
                            #print(f"右傳 {right_m_bB_left}, 食 {right_c_bB_left}, 左傳 {left_m_bB}, 食 {left_c_bB}")
                            #print(f"cost: {cost}, step: {step}\n")

    else :
        for boatA_operation in boatA_operations:
            # boat A on the left bank
            bA_state = np.array([curr_node.bA, bACost, bATime, 1]) #1: moving
            left_m_bA = left_m - boatA_operation[0] #left_m_bA左岸剩下的傳教士 (左岸原本的傳教士人數 - boatA載的傳教士人數)
            left_c_bA = left_c - boatA_operation[1] #left_c_bA左岸剩下的食人族 (左岸原本的食人族人數 - boatA載的食人族人數)
            right_m_bA_left = right_m + boatA_operation[0] #right_m_bA右岸所有的傳教士 (右岸原本的傳教士人數 + boatA載的傳教士人數)
            right_c_bA_left = right_c + boatA_operation[1] #right_c_bA右岸所有的食人族 (右岸原本的食人族人數 + boatA載的食人族人數)
            if (boatA_operation[0] + boatA_operation[1] == 0):
                bA_state = [-curr_node.bA, 0, 0, 0] #bA_pos, bACost, bATime, bAmove
            if is_safe(right_m_bA_left, right_c_bA_left) and left_m_bA + right_m_bA_left == totalM and left_c_bA + right_c_bA_left == totalC:
                if (curr_node.bB > 0): #boat B on the right bank 
                    for boatB_operation in boatB_operations:
                        bB_state = np.array([curr_node.bB, bBCost, bBTime, 1]) #1: moving
                        
                        right_m_bB_left = left_m_bA + boatB_operation[0] #right_m_bB左S岸所有的傳教士 (左岸原本的傳教士人數 + boatB載的傳教士人數)
                        right_c_bB_left = left_c_bA + boatB_operation[1] #right_c_bB左岸所有的食人族 (左岸原本的食人族人數 + boatB載的食人族人數)

                        right_m_bB = totalM - right_m_bB_left
                        right_c_bB = totalC - right_c_bB_left

                        if (boatB_operation[0] + boatB_operation[1] == 0):
                                bB_state = [-curr_node.bB, 0, 0, 0] #bB_pos, bBCost, bBTime, bBmove
                                #right_m - boatB_operation[0] >= 0 and right_c - boatB_operation[1] >= 0
                        if is_safe(right_m_bB,  right_c_bB) and not(bA_state[3] == 0 and bB_state[3] == 0) and right_m - boatB_operation[0] >= 0 and right_c - boatB_operation[1] >= 0 :
                            
                            step = curr_node.step + bA_state[2] + bB_state[2] - min(bA_state[2], bB_state[2]) #原本已經走的step加上boat A, boat B的step 減掉他們重疊的step
                            cost = curr_node.cost + bA_state[1] + bB_state[1]
                            successor.append(Node(right_m_bB, right_c_bB, -bA_state[0], bA_state[3], boatA_operation[0], boatA_operation[1], -bB_state[0], bB_state[3], boatB_operation[0], boatB_operation[1], step, cost, curr_node))
                            #print(f"boatA: m {boatA_operation[0]}, c {boatA_operation[1]}")
                            #print(f"boatB: m {boatB_operation[0]}, c {boatB_operation[1]}")
                            #print(f"右傳 {right_m_bB_left}, 食 {right_c_bB_left}, 左傳 {left_m_bB}, 食 {left_c_bB}")
                            #print(f"cost: {cost}, step: {step}\n")

                else: #boat B on the left bank
                    for boatB_operation in boatB_operations:
                        bB_state = np.array([curr_node.bB, bBCost, bBTime, 1]) #1: moving
            
                        left_m_bB =  left_m_bA - boatB_operation[0] #left_m_bA左岸剩下的傳教士 (左岸原本的傳教士人數 - boatA載的傳教士人數)
                        left_c_bB = left_c_bA - boatB_operation[1] #left_c_bA左岸剩下的食人族 (左岸原本的食人族人數 - boatB載的食人族人數)
                        right_m_bB_left = right_m_bA_left + boatB_operation[0] #right_m_bB右岸所有的傳教士 (右岸原本的傳教士人數 + boatB載的傳教士人數)
                        right_c_bB_left = right_c_bA_left + boatB_operation[1] #right_c_bB右岸所有的食人族 (右岸原本的食人族人數 + boatB載的食人族人數)

                        if (boatB_operation[0] + boatB_operation[1] == 0):
                                bB_state = [-curr_node.bB, 0, 0, 0] #bB_pos, bBCost, bBTime, bBmove
                                
                        if is_safe(right_m_bB_left, right_c_bB_left) and not(bA_state[3] == 0 and bB_state[3] == 0):
                            
                            step = curr_node.step + bA_state[2] + bB_state[2] - min(bA_state[2], bB_state[2]) #原本已經走的step加上boat A, boat B的step 減掉他們重疊的step
                            cost = curr_node.cost + bA_state[1] + bB_state[1]
                            successor.append(Node(right_m_bB_left, right_c_bB_left, -bA_state[0], bA_state[3], boatA_operation[0], boatA_operation[1], -bB_state[0], bB_state[3], boatB_operation[0], boatB_operation[1], step, cost, curr_node))
                            #print(f"boatA: m {boatA_operation[0]}, c {boatA_operation[1]}")
                            #print(f"boatB: m {boatB_operation[0]}, c {boatB_operation[1]}")
                            #print(f"右傳 {right_m_bB_left}, 食 {right_c_bB_left}, 左傳 {left_m_bB}, 食 {left_c_bB}")
                            #print(f"cost: {cost}, step: {step}\n")
    print(len(successor))
    for i in range(len(successor)):
        
        printNode(successor[i])
        print("")


start_node = Node(totalM, totalC, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, None)  # 初始狀態節點
get_all_children(start_node, 1, boatA_operations, boatB_operations)