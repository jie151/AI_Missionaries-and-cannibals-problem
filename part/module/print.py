import prettytable

def printNode(node, setting): # print node information
    print(f"right bank: m: {node.state['m']}, c: {node.state['c']}")
    print(f"left bank:  m: {setting['totalM'] - node.state['m']}, c: {setting['totalC'] - node.state['c']}")
    print(f"boat A: pos: {node.state['bA']}, move: {node.state['bAMove']}, m: {node.boatA['bA_m']}, c: {node.boatA['bA_c']}")
    print(f"boat B: pos: {node.state['bB']}, move: {node.state['bBMove']}, m: {node.boatB['bB_m']}, c: {node.boatB['bB_c']}")
    print(f"cost: {node.data[0]}, step: {node.data[1]}, h(n): {node.h}, f(n): {node.data[2]}\n")

def printTable(dataList, setting):
    table = prettytable.PrettyTable()
    table.field_names = ["step", "left m", "left c", "boatA DIR", "boatA [m c]", "boatB DIR", "boatB [m c]" , "right m", "right c", "cost", "AStar_h"]
    if not dataList:
        with open('table.txt', 'a') as w:
            w.write("no Solution!!!")
        return
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
    with open('table.txt', 'a') as w:
        w.write(str(table))
    #print(table)