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
