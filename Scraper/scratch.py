import io
import os
import os.path
from pathlib import Path

dataPath = "D:\\scrapeBoss\\f.txt"
scrapedPidPath = "D:\\scrapeBoss\\pid.txt"
scrapedTopicPath = "D:\\scrapeBoss\\topic.txt"
waitingPidPath = "D:\\scrapeBoss\\wpid.txt"
waitingTopicPath = "D:\\scrapeBoss\\wtopic.txt"

def loadList(path):
    with open(path, 'r', encoding='utf-8') as f:
        list = f.readlines()
        return [l[0:-1] for l in list]

def saveList(list, path):
    file = Path(path)
    if file.exists():
        os.remove(path)
    with open(path, 'w', encoding='utf-8') as writer:
        for line in list:
            writer.write(line + "\n")
    pass

def distinct(lis):
    hset = set()
    for l in lis:
        if not hset.__contains__(l):
            hset.add(l)
    return list(hset)

def buildscrapedqid():
    list = loadList(dataPath)
    list = distinct([l.split("\t")[0] for l in list])
    saveList(list, scrapedPidPath)
    pass
def buildwaitingqid():
    list = loadList(dataPath)
    list = distinct([l.split("\t")[0] for l in list[-500:]])
    saveList(list, waitingPidPath)
    pass
def buildscrapedtopic():
    ## list = loadList(dataPath)
    # list = distinct([l.split("\t")[4] for l in list])
    ## saveList(list, scrapedTopicPath)
    pass

def buildwaitingtopic():
    list = loadList(dataPath)
    outputlist = []
    for line in list:
        token = line.split("\t")
        outputlist.append(token[5])

    outputlist = distinct(outputlist)
    saveList(outputlist, waitingTopicPath)
    pass

def main():
    buildscrapedqid()
    buildwaitingqid()
    buildscrapedtopic()
    buildwaitingtopic()

if __name__ == "__main__":
    main()