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