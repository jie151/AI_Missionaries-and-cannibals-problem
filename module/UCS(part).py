import queue
import numpy as np
import prettytable
from node import Node
from generate_children import get_all_children
from sortNode import sortNode
from createBoatActions import boatA_actions, boatB_actions
from logFile import logging_file

totalM = int(input("請輸入傳教士的人數: ")) # total Missionaries (right bank)  
totalC = int(input("請輸入野人的人數: "))  # total cannibals (right bank) 
while totalM < totalC:
    totalM = int(input("請再次輸入傳教士的人數: ")) # total Missionaries (right bank)  
    totalC = int(input("請再次輸入野人的人數: "))  # total cannibals (right bank) 

costOrStep = int(input("cost輸入0, time輸入1: "))
bAMax = 2 # Boat A maximum capacities: 2 persons
bBMax = 3 # Boat B maximum capacities: 3 persons
bACost = 3  # fare
bBCost = 25 # fare
bATime = 1
bBTime = 1 
bAPos = 1 # right bank: 1, left bank: -1
bBPos = 1 # right bank: 1, left bank: -1

setting_state = np.array([totalM, totalC, costOrStep, bACost, bATime, bAMax, bBCost, bBTime, bBMax])

boatA_operations = boatA_actions(2, bACost, bATime)
boatB_operations = boatB_actions(3, bBCost, bBTime)

def printNode(node): # print node information
    print(f"right bank: m: {node.m}, c: {node.c}")
    print(f"left bank:  m: {totalM - node.m}, c: {totalC - node.c}")
    print(f"boat A: pos: {node.bA}, move: {node.bAMove}, m: {node.bA_m}, c: {node.bA_c}")
    print(f"boat B: pos: {node.bB}, move: {node.bBMove}, m: {node.bB_m}, c: {node.bB_c}")
    print(f"cost: {node.cost}, step: {node.step}\n")

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
        children = get_all_children(curr_node, boatA_operations, boatB_operations, setting_state) # cost: 0 , time: 1
        
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
uniform_cost_search(goal_node, start_node)