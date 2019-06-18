import os
import sys
import json

folderName = sys.argv[1]
folderPath = os.getcwd() + "\\" + folderName
print('folderPath', folderPath)

statistics = statistics = {
    "sent" : {
        "OK": 0,
        "ELECTION": 0,
        "LEADER": 0,
        "ALIVE": 0,
        "ALIVE_OK": 0,
        "JOIN_SWARM": 0,
        "GET_MEMBERS": 0,
        "KILL": 0
    },
    "received" : {
        "OK": 0,
        "ELECTION": 0,
        "LEADER": 0,
        "ALIVE": 0,
        "ALIVE_OK": 0,
        "JOIN_SWARM": 0,
        "GET_MEMBERS": 0,
        "KILL": 0
    }
}

def main():
    for innerFolder in os.listdir(folderPath):
        for filename in os.listdir(folderPath+'\\'+innerFolder):
            with open(folderPath+'\\'+innerFolder+'\\'+filename, 'r') as myFile:
                dic = json.load(myFile)
                sumDictionaryNumbers(statistics, dic)
    print(statistics)
    divDictionaryNumbers(statistics)
    print(statistics)

def sumDictionaryNumbers(firstDic, secondDic):
    for key, value in firstDic.items():
        if(isinstance(value,int)):
            firstDic[key] += secondDic[key]
            continue
        elif(isinstance(value,dict)):
            sumDictionaryNumbers(firstDic[key], secondDic[key])
            continue
        raise Exception('shouldnt come here!')

def divDictionaryNumbers(firstDic):
    for key, value in firstDic.items():
        if(isinstance(value,int)):
            firstDic[key] = firstDic[key]/10
            continue
        elif(isinstance(value,dict)):
            divDictionaryNumbers(firstDic[key])
            continue
        raise Exception('shouldnt come here!')

main()