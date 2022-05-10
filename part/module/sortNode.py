def sortNode (dataList, cost_or_time):
    for i in range(len(dataList)):
        for j in range(i, len(dataList)):
            change = 0
            if (dataList[i].data[cost_or_time] < dataList[j].data[cost_or_time]):
                change = 1
            elif (dataList[i].data[cost_or_time] == dataList[j].data[cost_or_time]) and cost_or_time== 1:
                if (dataList[i].data[0] < dataList[j].data[0]):
                    change = 1
            if change == 1:
                temp = dataList[i]
                dataList[i] = dataList[j]
                dataList[j] = temp
                
                    
