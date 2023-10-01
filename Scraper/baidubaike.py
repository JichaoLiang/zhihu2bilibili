from bs4 import BeautifulSoup
import requests
import json
import time
import randomNum
import io
import os.path
from pathlib import Path
import traceback
# import urllib.parse
import urllib
import urlparse
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

requestConfig = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "cookie": "lastCity=101010100; sid=sem_pz_bdpc_dasou_title; __g=sem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1656859923; Hm_lvt_f97992073bffedfa462561a24c99eb83=1656859926; wd_guid=cc8e9532-4f44-48c2-9535-31be86a90f2b; historyState=state; wljssdk_cross_new_user=1; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1656859962; wt2=DK6-CZbTlbdKFd4zsOaNwECsVo8RIpukEWjw5e3dPHGf7MBuTHee0Via5-9F4gKkGJ7--erfBecAIj9dVO9-Ytg~~; wbg=0; warlockjssdkcross={\"distinct_id\":\"52851058\",\"first_id\":\"181c48c1e62a36-00030193961745-6a7c2b1b-2073600-181c48c1e63100f\",\"props\":{},\"device_id\":\"181c48c1e62a36-00030193961745-6a7c2b1b-2073600-181c48c1e63100f\"}; __zp_seo_uuid__=f547d254-79c3-436f-897b-f5bf5eae0830; __l=r=https://youle.zhipin.com/questions/b8ce106c235ff3actnVy2dW5GVo~.html&l=/wapi/moment/preview/qrCode?bossUrl=https%3A%2F%2Fwww.zhipin.com%2Fmpa%2Fhtml%2Fget%2Fgrowth-system%2Findex&s=1; Hm_lpvt_f97992073bffedfa462561a24c99eb83=1656862905; __c=1656859923; __a=38993184.1656859923..1656859923.7.1.7.7"
}

targetUrl = {
    "list": "https://youle.zhipin.com/wapi/moment/pc/question/wait2Answer/tab?noFilterPosition=0&pageSize=10&page=[page_index]&isNew=0",
    "detailprefix": "https://youle.zhipin.com/questions/[qid].html",
    "topicprefix": "https://youle.zhipin.com/wapi/moment/pc/discover/feed/list?topicId=[topicid]&page=[pageindex]&sortType=0&filterType=2",
    "relatedtopicprefix": "https://youle.zhipin.com/topic/[topicid].html",
    "bingSearchPath": "https://cn.bing.com/search?[query]",
    "baikePrefix": "https://baike.baidu.com",
    "zhihufeedTemplate": "https://www.zhihu.com/api/v4/questions/[qid]/feeds?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=10&offset=0&order=default&platform=desktop",
    "zhihuSimilarTemplate": "https://www.zhihu.com/api/v4/questions/[qid]/similar-questions?include=data%5B*%5D.answer_count%2Cauthor%2Cfollower_count&limit=10",
    "zhihuQuestionPrefix": "https://www.zhihu.com/question/[qid]"
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
target = "D:\\scrapeBaike\\zhihu\\data"
# qidPath = "d:\\data.txt"
handler = None
lineCount = 0

qSet = set()
duplicated = 0

scrapedQid = set()
scrapedTopic = set()

scrapedQidPath = "D:\\scrapeBaike\\zhihu\\data\\zhihu_scraped.txt"
scrapedTopicPath = "D:\\scrapeBaike\\zhihu\\data\\scrapedTopic.txt"

waitQid = set()
waitingTopic = set()


qidQueue = []
topicQueue = []

waitQidPath = "D:\\scrapeBaike\\zhihu\\data\\catel3.txt.output.seedfound.zhihuQA"
waitTopicPath = "D:\\scrapeBaike\\zhihu\\data\\topicQueue.txt"

failedQid = set()
failedTopic = set()

failedQidPath = "D:\\scrapeBaike\\zhihu\\data\\zhihu_failed.txt"
failedTopicPath = "D:\\scrapeBaike\\zhihu\\faileTopic.txt"

flagPath = "D:\\scrapeBaike\\zhihu\\data\\stop.txt"
scrapeCounter = 0

# drop proxy ip when X times failure occurred
voteMaxThreshold = 10

topicInfoDict = {}


# seed finder section

seedQueryPath = "D:\\scrapeBaike\\data\\catel3.txt.output"
seedOutputPath = seedQueryPath + ".seedfound"
seedDict = set()
failedSeedList = set()

def stopFlag():
    return Path(flagPath).exists()

def saveList(list, path):
    file = Path(path)
    if file.exists():
        os.remove(path)
    with open(path, 'w') as writer:
        for line in list:
            writer.write(line + "\n")
    pass

def openf():
    global lineCount,index,handler,target
    pth = target+"_"+str(index)+".txt"
    # if not Path(pth).exists():
    #     open(Path(pth),'n',encoding='utf-8').close()
    handler = open(target+"_"+str(index)+".txt", 'a')
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


def scrapeMultiIterationGlobal(builderlist, callbacklist, alldonecallback):
    counter = 0
    maxRound = 2000000000
    while len(qidQueue) > 0 and counter < maxRound:
        print("qid queue: " + str(len(qidQueue)))
        print("topic queue: " + str(len(topicQueue)))
        print("Scraped: " + str(scrapeCounter))
        print("proxy survived: " + str(len(proxyList)))
        if len(proxyList) == 0:
            afterNoProxyStrategy(True)
            # return
        success = True
        global qidQueue
        task = qidQueue[0]
        qidQueue = qidQueue[1:]
        if waitQid.__contains__(task):
            waitQid.remove(task)

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
        task = taskQueue[0]
        taskQueue = taskQueue[1:]
        if taskSet.__contains__(task):
            taskSet.remove(task)
        while tried < retry:
            if len(proxyList) == 0:
                afterNoProxyStrategy(True)
            proxy = proxyList[int(random.random() * len(proxyList))]
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

def scrapeGlobal(builder, callback):
    retry = 3
    global qidQueue,waitQid
    while len(qidQueue) > 0:
        print("qid queue: " + str(len(qidQueue)))
        print("topic queue: " + str(len(topicQueue)))
        tried = 0
        success = False
        takebreak = False
        print("Scraped: " + str(scrapeCounter))
        print("Proxy survived: " + str(len(proxyList)))
        if len(proxyList) == 0:
            afterNoProxyStrategy(True)
        task = qidQueue[0]
        qidQueue = qidQueue[1:]
        if waitQid.__contains__(task):
            waitQid.remove(task)
        while tried < retry:
            if len(proxyList) == 0:
                afterNoProxyStrategy(True)
            proxy = proxyList[int(random.random() * len(proxyList))]
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
    try:
        with open(path, 'r') as f:
            list = f.readlines()
            return list
    except Exception as ex:
        return []

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

def scrapeZhihudetail():
    funcList = []
    def buildRequest(topicId):
        id = topicId.split('/')[-1].split('?')[0]
        url = targetUrl["zhihufeedTemplate"].replace("[qid]", id)
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRequest)
    def buildRelatedSearchRequest(topicId):
        id = topicId.split('/')[-1].split('?')[0]
        url = targetUrl["zhihuSimilarTemplate"].replace("[qid]", id)
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    funcList.append(buildRelatedSearchRequest)

    callbackList = []
    def recordAndDiscover(response, topicid):
        dataStr = response.text
        qnaList = json.loads(dataStr)["data"]
        for qna in qnaList:
            target = qna["target"]
            answer = target["excerpt"]
            voteup_count = target["voteup_count"]
            questionInfo = target["question"]
            questionTitle = questionInfo["title"]
            # questionId = questionInfo["url"]
            # if not scrapedQid.__contains__(questionId) and not waitQid.__contains__(questionId):
            msg = topicid + "\t" + questionTitle + "\t" + str(answer) + "\t" + str(voteup_count)
            print(msg)
            record(msg)
            # newQid(questionId

        # state saving (in alldone)
        # if not scrapedQid.__contains__(topicid):
        #     scrapedQid.add(topicid)

        return False,True
        pass
    callbackList.append(recordAndDiscover)

    def discover(response, topicid):
        dataStr = response.text
        entry = json.loads(dataStr)
        data = entry["data"]
        for dt in data:
            newId = dt["id"]
            newId = targetUrl["zhihuQuestionPrefix"].replace("[qid]", str(newId))
            newText = dt["title"]
            answerCount = dt["answer_count"]
            if answerCount == 0:
                continue
            if not scrapedTopic.__contains__(newId) and not waitingTopic.__contains__(newId):
                print("new: " + newText)
            newQid(newId)
        return False,True
        pass
    callbackList.append(discover)

    def alldone(topicid, success):
        if success:
            if not scrapedQid.__contains__(topicid):
                scrapedQid.add(topicid)
        else:
            if not failedQid.__contains__(topicid):
                failedQid.add(topicid)

    scrapeMultiIterationGlobal(funcList, callbackList, alldone)
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


def stripHtmlTag(p):
    tokens = []
    while p.__contains__('<') or p.__contains__('>'):
        tks = p.split('<')
        tokens.append(tks[0])
        p = '<'.join(tks[1:])
        tks = p.split('>')
        p = '>'.join(tks[1:])
    tokens.append(p)
    return ''.join(tokens)
    pass

def discoverLink(p):
    links = p.select('a')
    resultlist = []
    for link in links:
        if link.attrs.keys().__contains__('href') and link.attrs['href'].startswith('/item/'):
            href = link.attrs['href']
            resultlist.append(targetUrl["baikePrefix"] + href)
    return resultlist

def scrapeBossDetail():
    def buildRequest(qid):
        id = qid.split('/')[-1]
        url = targetUrl["zhihufeedTemplate"].replace("[qid]", id)
        # url = qid # targetUrl["detailprefix"].replace("[qid]", qid)
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header

    def recordAndDiscover(response, qid):
        dataStr = response.text
        bs = BeautifulSoup(dataStr, 'html.parser')
        summary = bs.select(".lemma-summary")
        title = bs.select(".J-lemma-title")
        titleStr = ""
        if len(title) > 0:
            h1 = title[0].select("h1")
            if len(h1) > 0:
                titleStr = stripHtmlTag(h1[0].text)
        if len(summary) > 0:
            paragraphs = summary[0].select('.para')
            SummaryList = []
            for p in paragraphs:
                SummaryList.append(stripHtmlTag(p.text))
                newLink = discoverLink(p)
                for l in newLink:
                    newQid(l)
            joinedStr = convertNewLineAndTable('[SEP]'.join([p.text for p in paragraphs]))
            outputLine = titleStr + "\t" + joinedStr
            print(outputLine)
            record(outputLine)
        # state saving
        if not scrapedQid.__contains__(qid):
            scrapedQid.add(qid)

        return False, True
    # stripedQueue = [q[-1] for q in qidQueue]
    scrapeGlobal(buildRequest, recordAndDiscover)
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
                print("found " + str(len(list)))
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


def zhihuPickedRulePassed(siteUrl):
    if siteUrl.startswith('https://zhidao.baidu.com'):
        return True
    if siteUrl.startswith('https://baike.baidu.com'):
        return True
    if siteUrl.startswith('https://www.zhihu.com'):
        return True
    pass


def scrapeSeedUrlBykey():
    querylist = loadList(seedQueryPath)
    def builder(task):
        urlTemplate = targetUrl["bingSearchPath"]
        url = urlTemplate.replace("[query]", urllib.urlencode({'q': task}))
        header = {"user-agent": requestConfig["user-agent"]}
        return url, header
    def callback(response, id):
        textStr = response.text
        bs = BeautifulSoup(textStr, 'html.parser')
        ol = bs.select('#b_results')[0]
        lis = ol.select('.b_algo')
        for li in lis:
            try:
                st = li.select('cite')
                if len(st) > 0:
                    site = st[0]
                    siteUrl = site.text
                    if zhihuPickedRulePassed(siteUrl):
                        key = id + "\t" + siteUrl
                        if not seedDict.__contains__(key):
                            print(key)
                            seedDict.add(id+"\t"+siteUrl)
            except Exception as ex:
                print(str(ex))
        return False, True
    for query in querylist:
        task = query.replace('\n', '')
        try:
            scrapeSingle(task, builder, callback)
        except Exception as ex:
            print(str(ex))
            failedSeedList.add(id)
    saveList(list(seedDict),seedOutputPath)
    pass

def main():
    # scrapeSeedUrlBykey()
    restoreScrapeDataQueue()
    # scrapeBossQuestionListByTopic()
    scrapeZhihudetail()
    # scrapeBossDetail()
    # scrapeBossList()

openf()
main()
closef()
