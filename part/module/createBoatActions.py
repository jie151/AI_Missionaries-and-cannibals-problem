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