def sortNode (dataList, cost_or_time):
    for i in range(len(dataList)):
        for j in range(i, len(dataList)):
            if (dataList[i].data[cost_or_time] < dataList[j].data[cost_or_time]):
                temp = dataList[i]
                dataList[i] = dataList[j]
                dataList[j] = temp  