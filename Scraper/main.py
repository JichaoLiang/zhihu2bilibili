from bs4 import BeautifulSoup
import requests
import json
import time
import randomNum
import io
import os.path
from pathlib import Path
import traceback

requestConfig = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "cookie": "lastCity=101010100; sid=sem_pz_bdpc_dasou_title; __g=sem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1656859923; Hm_lvt_f97992073bffedfa462561a24c99eb83=1656859926; wd_guid=cc8e9532-4f44-48c2-9535-31be86a90f2b; historyState=state; wljssdk_cross_new_user=1; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1656859962; wt2=DK6-CZbTlbdKFd4zsOaNwECsVo8RIpukEWjw5e3dPHGf7MBuTHee0Via5-9F4gKkGJ7--erfBecAIj9dVO9-Ytg~~; wbg=0; warlockjssdkcross={\"distinct_id\":\"52851058\",\"first_id\":\"181c48c1e62a36-00030193961745-6a7c2b1b-2073600-181c48c1e63100f\",\"props\":{},\"device_id\":\"181c48c1e62a36-00030193961745-6a7c2b1b-2073600-181c48c1e63100f\"}; __zp_seo_uuid__=f547d254-79c3-436f-897b-f5bf5eae0830; __l=r=https://youle.zhipin.com/questions/b8ce106c235ff3actnVy2dW5GVo~.html&l=/wapi/moment/preview/qrCode?bossUrl=https%3A%2F%2Fwww.zhipin.com%2Fmpa%2Fhtml%2Fget%2Fgrowth-system%2Findex&s=1; Hm_lpvt_f97992073bffedfa462561a24c99eb83=1656862905; __c=1656859923; __a=38993184.1656859923..1656859923.7.1.7.7"
}

targetUrl = {
    "list": "https://youle.zhipin.com/wapi/moment/pc/question/wait2Answer/tab?noFilterPosition=0&pageSize=10&page=[page_index]&isNew=0",
    "detailprefix":"https://youle.zhipin.com/questions/[qid].html",
    "topicprefix":"https://youle.zhipin.com/wapi/moment/pc/discover/feed/list?topicId=[topicid]&page=[pageindex]&sortType=0&filterType=2",
    "relatedtopicprefix":"https://youle.zhipin.com/topic/[topicid].html"
}

proxyList = [
    {"http": "111.225.152.157:8089"},
    {"http": "101.6.58.216:6666"},
    {"http": "49.85.15.189:9000"},
    {"http": "183.154.214.74:9000"},
    {"http": "122.243.14.38:9000"},
    {"http": "111.3.118.247:30001"},
    {"http": "114.234.25.54:8901"},
    {"http": "171.92.20.24:9000"},
    {"http": "171.92.21.202:9000"},
    {"http": "125.67.174.172:7890"},
    {"http": "115.211.33.105:9000"},
    {"http": "218.89.51.167:9091"},
    {"http": "171.92.21.180:9000"},
    {"http": "124.222.77.10:8080"},
    {"http": "58.251.98.105:3129"},
    {"http": "182.139.110.74:9000"},
    {"http": "211.103.138.117:8000"},
    {"http": "115.211.39.104:9000"},
    {"http": "39.108.101.55:1080"},
    {"http": "103.178.42.10:8181"},
    {"http": "39.175.75.53:30001"},
    {"http": "112.74.17.146:8118"},
    {"http": "114.67.104.36:18888"},
    {"http": "222.79.63.199:9999"},
    {"http": "183.247.211.50:30001"},
    {"http": "182.139.110.74:8089"},
    {"http": "101.6.58.216:6666"},
    {"http": "49.85.15.189:9000"},
    {"http": "183.154.214.74:9000"},
    {"http": "122.243.14.38:9000"},
    {"http": "111.3.118.247:30001"},
    {"http": "114.234.25.54:8901"},
    {"http": "171.92.20.24:9000"},
    {"http": "171.92.21.202:9000"},
    {"http": "125.67.174.172:7890"},
    {"http": "115.211.33.105:9000"},
    {"http": "218.89.51.167:9091"},
    {"http": "171.92.21.180:9000"},
    {"http": "124.222.77.10:8080"},
    {"http": "58.251.98.105:3129"},
    {"http": "182.139.110.74:9000"},
    {"http": "211.103.138.117:8000"},
    {"http": "115.211.39.104:9000"},
    {"http": "39.108.101.55:1080"},
    {"http": "103.178.42.10:8181"},
    {"http": "39.175.75.53:30001"},
    {"http": "112.74.17.146:8118"},
    {"http": "114.67.104.36:18888"},
    {"http": "222.79.63.199:9999"},
    {"http": "183.247.211.50:30001"},
    {"http": "113.90.178.118:7890"},
    {"http": "111.72.154.171:7082"},
    {"http": "115.212.126.252:9000"},
    {"http": "124.226.194.135:808"},
    {"http": "113.111.0.183:808"},
    {"http": "121.13.252.58:41564"},
    {"http": "115.223.221.194:9000"},
    {"http": "115.210.31.0:9000"},
    {"http": "124.16.103.122:4780"},
    {"http": "111.225.153.137:8089"},
    {"http": "106.75.73.56:80"},
    {"http": "111.229.161.172:888"},
    {"http": "113.111.140.50:808"},
    {"http": "183.173.123.32:7890"},
    {"http": "115.211.34.89:9000"},
    {"http": "115.211.41.103:9000"},
    {"http": "163.142.146.241:8118"},
    {"http": "124.205.155.154:9090"},
    {"http": "183.245.6.123:8080"},
    {"http": "61.153.251.150:22222"},
    {"http": "49.85.94.125:9000"},
    {"http": "58.240.110.171:8888"},
    {"http": "124.205.155.152:9090"},
    {"http": "182.92.77.108:8081"},
    {"http": "115.211.45.26:9000"}
]

proxyVoteDict={

}

for i in range(0, len(proxyList)):
    proxyVoteDict.setdefault(proxyList[i]["http"], 0)

index = 0
maxLine = 10000
# target = "R:\\scrapeBoss\\data"
topicInfoPath = "d:\\scrapeBoss\\topic.txt"
target = "d:\\scrapeBoss\\data"
# qidPath = "d:\\data.txt"
handler = None
lineCount = 0

qSet = set()
duplicated = 0

scrapedQid = set()
scrapedTopic = set()

scrapedQidPath = "d:\\scrapeBoss\\scrapedQid.txt"
scrapedTopicPath = "d:\\scrapeBoss\\scrapedTopic.txt"

waitQid = set()
waitingTopic = set()


qidQueue = []
topicQueue = []

waitQidPath = "d:\\scrapeBoss\\qidQueue.txt"
waitTopicPath = "d:\\scrapeBoss\\topicQueue.txt"

failedQid = set()
failedTopic = set()

failedQidPath = "d:\\scrapeBoss\\faileQid.txt"
failedTopicPath = "d:\\scrapeBoss\\faileTopic.txt"

flagPath = "d:\\scrapeBoss\\stop.txt"
scrapeCounter = 0

# drop proxy ip when X times failure occurred
voteMaxThreshold = 10

topicInfoDict = {}

def stopFlag():
    return Path(flagPath).exists()

def saveList(list, path):
    file = Path(path)
    if file.exists():
        os.remove(path)
    with open(path, 'w', encoding='utf-8') as writer:
        for line in list:
            writer.write(line + "\n")
    pass

def openf():
    global lineCount,index,handler,target
    pth = target+"_"+str(index)+".txt"
    # if not Path(pth).exists():
    #     open(Path(pth),'n',encoding='utf-8').close()
    handler = open(target+"_"+str(index)+".txt", 'a', encoding='utf-8')
    index += 1
    lineCount = 0

def closef():
    global handler
    handler.close()

def record(msg):
    global handler,lineCount
    handler.write(msg + "\n")
    lineCount += 1
    if lineCount > maxLine:
        closef()
        openf()

def saveStatus():
    saveList(list(scrapedQid), scrapedQidPath)
    saveList(list(scrapedTopic), scrapedTopicPath)
    saveList(qidQueue, waitQidPath)
    saveList(topicQueue, waitTopicPath)
    saveList(failedQid, failedQidPath)
    saveList(failedTopic, failedTopicPath)


def voteAndBlacklistProxy(proxyVal):
    key = proxyVal["http"]
    voteVal = proxyVoteDict.get(key)
    if voteVal < voteMaxThreshold:
        proxyVoteDict[key] = proxyVoteDict[key] + 1
    else:
        for i in range(0, len(proxyList)):
            if proxyList[i]["http"] == key:
                print("proxy: " + key + " is turned off. left: " + str(len(proxyList)))
                proxyList.pop(i)
                break
    pass

def afterNoProxyStrategy(keepGoing):
    if keepGoing:
        for k in proxyVoteDict.keys():
            proxyVoteDict[k] = 0
            entry = {"http": k}
            if not proxyList.__contains__(entry):
                proxyList.append(entry)
    else:
        saveStatus()

def scrapeSingle(task, builder, callback):
    retry = 3
    tried = 0
    takebreak = False
    success = True
    while tried < retry:
        proxy = proxyList[int(random.random() * len(proxyList))]
        if len(proxyList) == 0:
            afterNoProxyStrategy(True)
            # return
        try:
            url, header = builder(task)
            response = requests.get(url, headers=header, proxies=proxy)
            takebreak, keepGoing = callback(response, task)
            if not keepGoing:
                return
            success = True
            break
        except Exception as e:
            success = False
            tried += 1
            stack = traceback.format_exc()
            print(str(e))
            print(stack)
            print(task)
            voteAndBlacklistProxy(proxy)

        if takebreak:
            time.sleep(21)
    return success

def scrapeMultiIteration(taskQueue, taskSet, builderlist, callbacklist, alldonecallback):
    counter = 0
    maxRound = 2000
    while len(taskQueue) > 0 and counter < maxRound:
        print("qid queue: " + str(len(qidQueue)))
        print("topic queue: " + str(len(topicQueue)))
        print("Scraped: " + str(scrapeCounter))
        print("proxy survived: " + str(len(proxyList)))
        if len(proxyList) == 0:
            afterNoProxyStrategy(True)
            # return
        success = True
        task = taskQueue.pop()
        taskSet.remove(task)

        for i in range(0,len(builderlist)):
            builder = builderlist[i]
            callback = callbacklist[i]
            s = scrapeSingle(task, builder, callback)
            if not s:
                success = False
            time.sleep(int(random.random() * 3))

        alldonecallback(task, success)
        if stopFlag():
            return
        counter += 1
        if counter % 50 == 0:
            saveStatus()
            try:
                saveTopicInfo()
            except Exception as e:
                print(e)
                stack = traceback.format_exc()
                print(stack)
    pass

def scrape(taskQueue, taskSet, builder, callback):
    retry = 3

    while len(taskQueue) > 0:
        print("qid queue: " + str(len(qidQueue)))
        print("topic queue: " + str(len(topicQueue)))
        tried = 0
        success = False
        takebreak = False
        print("Scraped: " + str(scrapeCounter))
        print("Proxy survived: " + str(len(proxyList)))
        if len(proxyList) == 0:
            afterNoProxyStrategy(True)
        task = taskQueue.pop()
        taskSet.remove(task)
        while tried < retry:
            if len(proxyList) == 0:
                afterNoProxyStrategy(True)
            proxy=proxyList[int(random.random() * len(proxyList))]
            try:
                url, header = builder(task)
                response = requests.get(url, headers=header, proxies=proxy)
                takebreak, keepGoing = callback(response, task)
                success = True
                if not keepGoing:
                    return
                break
            except Exception as e:
                success = False
                tried += 1
                stack = traceback.format_exc()
                print(str(e))
                print(stack)
                print(task)
                voteAndBlacklistProxy(proxy)
        if not success:
            if not failedQid.__contains__(task):
                failedQid.add(task)
        if stopFlag():
            return
        if takebreak:
            time.sleep(21)
        time.sleep(int(random.random() * 3))

    pass

def loadList(path):
    with open(path, 'r', encoding='utf-8') as f:
        list = f.readlines()
        return list

# def prepareQidList():
#     list = loadList(qidPath)
#     result = []
#     for item in list:
#         if len(item) > 2:
#             result.append(item)
#     return [item.split("https://youle.zhipin.com/questions/")[-1].split(".html")[0] for item in result]

def stripId(str):
    return str.split("https://youle.zhipin.com/questions/")[-1].split(".html")[0]

def stripTopic(str):
    return str.split("https://youle.zhipin.com/topic/")[-1].split(".html")[0]

def restoreScrapeDataQueue():
    list = [l.replace('\n','') for l in loadList(waitQidPath)]
    for l in list:
        waitQid.add(l)
        qidQueue.append(l)

    list = [l.replace('\n','') for l in loadList(waitTopicPath)]
    for l in list:
        waitingTopic.add(l)
        topicQueue.append(l)

    list = [l.replace('\n','') for l in loadList(scrapedQidPath)]
    for l in list:
        scrapedQid.add(l)

    list = [l.replace('\n','') for l in loadList(scrapedTopicPath)]
    for l in list:
        scrapedTopic.add(l)

def scrapeBossRelatedTopic():
    pass

def scrapeBossQuestionListByTopic():
    funcList = []
    def buildRequest(topicId):
        url = targetUrl["topicprefix"].replace("[topicid]", topicId).replace('[pageindex]', str(1))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)
    def buildRequest(topicId):
        url = targetUrl["topicprefix"].replace("[topicid]", topicId).replace('[pageindex]', str(2))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)
    def buildRequest(topicId):
        url = targetUrl["topicprefix"].replace("[topicid]", topicId).replace('[pageindex]', str(3))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)
    def buildRequest(topicId):
        url = targetUrl["topicprefix"].replace("[topicid]", topicId).replace('[pageindex]', str(4))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)
    def buildRequest(topicId):
        url = targetUrl["topicprefix"].replace("[topicid]", topicId).replace('[pageindex]', str(5))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)
    def buildRequest(topicId):
        url = targetUrl["topicprefix"].replace("[topicid]", topicId).replace('[pageindex]', str(6))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)
    def buildRequest(topicId):
        url = targetUrl["topicprefix"].replace("[topicid]", topicId).replace('[pageindex]', str(7))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)
    def buildRequest(topicId):
        url = targetUrl["topicprefix"].replace("[topicid]", topicId).replace('[pageindex]', str(8))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)
    def buildRequest(topicId):
        url = targetUrl["topicprefix"].replace("[topicid]", topicId).replace('[pageindex]', str(9))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)
    def buildRequest(topicId):
        url = targetUrl["topicprefix"].replace("[topicid]", topicId).replace('[pageindex]', str(10))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)

    def buildRelatedSearchRequest(topicId):
        url = targetUrl["relatedtopicprefix"].replace("[topicid]", topicId)
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRelatedSearchRequest)

    callbackList = []
    for i in range(0, 10):
        def recordAndDiscover(response, topicid):
            dataStr = response.text
            data = json.loads(dataStr)
            qnaList = data["zpData"]["list"]
            for qna in qnaList:
                questionInfo = qna["questionInfo"]
                content = questionInfo["content"]
                answerCount = questionInfo["answerCount"]
                questionId = questionInfo["questionId"]
                if not scrapedQid.__contains__(questionId) and not waitQid.__contains__(questionId):
                    print(questionId + "\t" + content + "\t" + str(answerCount))
                newQid(questionId)
            return False,True
        callbackList.append(recordAndDiscover)

    def recordAndDiscoverNewTopic(response, topicid):
        dataStr = response.text
        bs = BeautifulSoup(dataStr, 'html.parser')
        ul = bs.select('.related-list')[0]
        li_list = ul.select('.topicItem')
        for li in li_list:
            relatedTopicId = stripTopic(li.a["href"])
            relatedTopicName = li.a.text.replace("\n","").strip()
            countInfo = li.select(".count_info > span")
            questionCount = countInfo[0].text
            focusCount = countInfo[1].text
            topicInfoToDict(relatedTopicId, relatedTopicName, questionCount, focusCount)
            if not scrapedTopic.__contains__(relatedTopicId) and not waitingTopic.__contains__(relatedTopicId):
                print(relatedTopicId + "\t" + relatedTopicName + "\t" + questionCount + "\t" + focusCount)
            newTopic(relatedTopicId)
        return False,True
    callbackList.append(recordAndDiscoverNewTopic)

    def alldone(topicid, success):
        if success:
            if not scrapedTopic.__contains__(topicid):
                scrapedTopic.add(topicid)
        else:
            if not failedTopic.__contains__(topicid):
                failedTopic.add(topicid)

    scrapeMultiIteration(topicQueue, waitingTopic, funcList, callbackList, alldone)
    saveStatus()
    pass

def topicInfoToDict(topicId, topicName, qCount, fCount):
    if topicInfoDict.get(topicId) == None:
        topicInfoDict.setdefault(topicId, [topicName, qCount, fCount])


def saveTopicInfo():
    with open(topicInfoPath,'a') as f:
        for k in topicInfoDict.keys():
            val = topicInfoDict.get(k)
            f.write(k + "\t" + val[0] + "\t" + str(val[1]) + "\t" + str(val[2]) + "\n")

def convertNewLineAndTable(str):
    return str.replace('\n','<br />').replace('\t', '&nbsp;')

def scrapeBossDetail():
    def buildRequest(qid):
        url = targetUrl["detailprefix"].replace("[qid]", qid)
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header

    def recordAndDiscover(response, qid):
        dataStr = response.text
        bs = BeautifulSoup(dataStr, 'html.parser')
        node = bs.find_all(id="page-main-content")[0]
        qna = node.select('.page-main-width-side > div')
        # print(len(qna))
        # print(qna[0].select('.question-title > span'))
        question = convertNewLineAndTable(qna[0].select('.question-title > span')[0].text)
        role = str.strip(qna[0].select('.subTitle')[0].text.replace('\n', ''))
        questionDetailNode = qna[0].select('.question-detail')
        questionDetail = ''
        if len(questionDetailNode) > 1:
            questionDetail = convertNewLineAndTable(questionDetailNode[1].text)
        topic = ""
        topicNode = qna[0].select('.topic > a')
        topicId = ""
        if len(topicNode) > 0:
            topic = topicNode[0].text
            topicId = stripTopic(topicNode[0]['href'])
        answers = qna[1].select('li')
        answerList = []

        order = 0
        for answer in answers:
            # not answer li
            if len(answer.select('.real-text')) == 0:
                continue

            # role
            answerRole = ''
            if len(answer.select('.subTitle')) > 0:
                answerRole = answer.select('.subTitle')[0].text.replace('\n', '').strip()

            # answer text
            answerText = ''
            if len(answer.select('.real-text')) > 0:
                answerText = convertNewLineAndTable(answer.select('.real-text')[0].text)

            # rank
            footer = answer.select('.card-bottom-list > button')
            rank = 0
            if len(footer) > 0 and len(footer[0].select('span')) > 0:
                rankStr = footer[0].select('span')[0].text
                try:
                    rank = int(rankStr)
                except Exception as e:
                    rank = 0
            answerList.append({"role": answerRole, "content": answerText, "order": order, "rank": rank})
            order += 1

        print(question + '\t' + role + '\t' + questionDetail + '\t' + topic + '\t' + str(len(answerList)))
        global scrapedQid,waitingTopic
        if not scrapedQid.__contains__(qid):
            for a in answerList:
                print(a["content"] + "\t" + a["role"] + "\t" + str(a["order"]) + "\t" + str(a["rank"]))
                recordeStr = qid + "\t" + question + '\t' + role + '\t' + questionDetail + '\t' + topic + "\t" + topicId + '\t' + str(len(answerList)) + "\t" + a["content"] + "\t" + a["role"] + "\t" + str(a["order"]) + "\t" + str(a["rank"])
                record(recordeStr)
                global scrapeCounter
                scrapeCounter += 1
        else:
            print("already exists in scraped set: " + qid)

        #state saving
        if not scrapedQid.__contains__(qid):
            scrapedQid.add(qid)

        # discover

        relatedList = bs.select(".related-list")[0]
        listItemRelated = relatedList.select('li > a')
        relatedIdList = []
        for item in listItemRelated:
            r_qid = stripId(item['href'])
            relatedIdList.append(r_qid)

        # insert queue
        newTopic(topicId)
        for r_qid in relatedIdList:
            newQid(r_qid)
        return False,True
    scrape(qidQueue , waitQid, buildRequest, recordAndDiscover)
    saveStatus()

def newQid(qid):
    if not scrapedQid.__contains__(qid) and not waitQid.__contains__(qid):
        waitQid.add(qid)
        qidQueue.append(qid)

def newTopic(topicId):
    if not scrapedTopic.__contains__(topicId) and not waitingTopic.__contains__(topicId) and len(topicId) > 0:
        waitingTopic.add(topicId)
        topicQueue.append(topicId)

def scrapeBossList():
    iter = 1
    retry = 3

    while iter < 200000:
        print(str(iter) + "/200000")
        tried = 0
        alldup = False
        while tried < retry:
            try:
                prox = proxyList[int(random.random() * len(proxyList))]
                response = requests.get(targetUrl["list"].replace("[page_index]", str(iter)), headers={"user-agent":requestConfig["user-agent"], "cookie":requestConfig["cookie"]})
                data = json.loads(response.text)
                list = None
                if "filterVO" in data["zpData"].keys() and len(data["zpData"]["filterVO"]["list"]) > 0:
                    list = data["zpData"]["filterVO"]["list"]
                elif "recVO" in data["zpData"].keys():
                    list = data["zpData"]["recVO"]["list"]
                    print("No filters. Using rec")
                else:
                    raise Exception("no key found")
                print("found "+ str(len(list)))
                dupCount = 0
                for item in list:
                        question = item["questionInfo"]["content"]
                        qUrl = targetUrl["detailprefix"].replace("[qid]", str(item["questionInfo"]["linkUrl"]).split("questionId=")[-1].split("&")[0])
                        answerCount = item["questionInfo"]["answerCount"]
                        topic = item["topicName"]
                        if qSet.__contains__(question):
                            global duplicated
                            duplicated += 1
                            dupCount += 1
                            print("dup: " + str(duplicated))
                        else:
                            qSet.add(question)
                            record(question+"\t"+qUrl+"\t"+str(answerCount)+"\t"+topic)
                            # print(question+"\t"+qUrl+"\t"+str(answerCount))
                alldup = dupCount == len(list)
                break
            except Exception as e:
                tried += 1
                print(str(e))
        iter += 1
        if alldup:
            time.sleep(21)
            iter = 1
        time.sleep(int(random.random() * 3))
    pass

def main():
    restoreScrapeDataQueue()
    scrapeBossQuestionListByTopic()
    scrapeBossDetail()
    # scrapeBossList()

openf()
main()
closef()
