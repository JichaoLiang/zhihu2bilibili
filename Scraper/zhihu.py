import random
from importlib import reload

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
import re
import sys
import Scraper.Analyser
from Scraper.Analyser.QuestionAnalyser import QuestionAnalyser
from Scraper.Analyser.AnswerAnalyser import AnswerAnalyser
from Scraper.Analyser.RelatedQuestionAnalyser import RelatedQuestionAnalyser
from Scraper.Analyser.FavorListAnalyser import FavorListAnalyser
from Scraper.Analyser.TopicAnalyser import TopicAnalyser
from Utils.CommonUtils import CommonUtils
from Utils.ZhihuTaskManager import ZhihuTaskManager
#
# reload(sys)
# sys.setdefaultencoding('utf-8')

requestConfig = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "cookie": "lastCity=101010100; sid=sem_pz_bdpc_dasou_title; __g=sem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1656859923; Hm_lvt_f97992073bffedfa462561a24c99eb83=1656859926; wd_guid=cc8e9532-4f44-48c2-9535-31be86a90f2b; historyState=state; wljssdk_cross_new_user=1; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1656859962; wt2=DK6-CZbTlbdKFd4zsOaNwECsVo8RIpukEWjw5e3dPHGf7MBuTHee0Via5-9F4gKkGJ7--erfBecAIj9dVO9-Ytg~~; wbg=0; warlockjssdkcross={\"distinct_id\":\"52851058\",\"first_id\":\"181c48c1e62a36-00030193961745-6a7c2b1b-2073600-181c48c1e63100f\",\"props\":{},\"device_id\":\"181c48c1e62a36-00030193961745-6a7c2b1b-2073600-181c48c1e63100f\"}; __zp_seo_uuid__=f547d254-79c3-436f-897b-f5bf5eae0830; __l=r=https://youle.zhipin.com/questions/b8ce106c235ff3actnVy2dW5GVo~.html&l=/wapi/moment/preview/qrCode?bossUrl=https%3A%2F%2Fwww.zhipin.com%2Fmpa%2Fhtml%2Fget%2Fgrowth-system%2Findex&s=1; Hm_lpvt_f97992073bffedfa462561a24c99eb83=1656862905; __c=1656859923; __a=38993184.1656859923..1656859923.7.1.7.7"
}

targetUrl = {
    "list": "https://youle.zhipin.com/wapi/moment/pc/question/wait2Answer/tab?noFilterPosition=0&pageSize=10&page=[page_index]&isNew=0",
    "detailprefix": "https://youle.zhipin.com/questions/[qid].html",
    "topicprefix": "https://youle.zhipin.com/wapi/moment/pc/discover/feed/list?topicId=[topicid]&page=[pageindex]&sortType=0&filterType=2",
    "relatedtopicprefix": "https://youle.zhipin.com/topic/[topicid].html",
    "bingSearchPath": "https://cn.bing.com/search?[query]",
    "baikePrefix": "https://baike.baidu.com"
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


handler = None
lineCount = 0

qSet = set()
duplicated = 0

#
# qidQueue = []
# topicQueue = []


dataBasePath = os.path.abspath('../Resource/task/zhihu/')
target = os.path.join(dataBasePath, 'data/data')

flagPath = os.path.join(dataBasePath, "stop.txt")
scrapeCounter = 0

# drop proxy ip when X times failure occurred
voteMaxThreshold = 10

topicInfoDict = {}


# seed finder section

# seedQueryPath = os.path.join(target, "母婴.output")
# seedOutputPath = seedQueryPath + ".seedfound"
# seedDict = set()
# failedSeedList = set()

def stopFlag():
    return Path(flagPath).exists()


def openf():
    global lineCount,index,handler,target
    pth = target+"_"+str(index)+".txt"
    if not Path(pth).exists():
        open(Path(pth),'x',encoding='utf-8').close()
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
        ZhihuTaskManager.saveStatus()

rand = random.Random()
def randNum():
    return rand.random()

def scrapeSingle(task, builder, callback):
    retry = 3
    tried = 0
    takebreak = False
    success = True
    while tried < retry:
        proxy = proxyList[int(randNum() * len(proxyList))]
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
        print("task queue: " + str(len(ZhihuTaskManager.taskQueue)))
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
            time.sleep(int(randNum() * 3))

        alldonecallback(task, success)
        if stopFlag():
            return
        counter += 1
        if counter % 50 == 0:
            ZhihuTaskManager.saveStatus()
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
        print("topic queue: " + str(len(ZhihuTaskManager.taskQueue)))
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
            proxy = proxyList[int(randNum() * len(proxyList))]
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
            ZhihuTaskManager.failedTask(task)
        if stopFlag():
            return
        if takebreak:
            time.sleep(21)
        time.sleep(int(randNum() * 3))

    pass

def scrapeGlobal(builder, callback):
    retry = 3
    while len(ZhihuTaskManager.taskQueue) > 0:
        print("qid queue: " + str(len(ZhihuTaskManager.taskQueue)))
        tried = 0
        success = False
        takebreak = False
        print("Scraped: " + str(scrapeCounter))
        print("Proxy survived: " + str(len(proxyList)))
        if len(proxyList) == 0:
            afterNoProxyStrategy(True)
        task = ZhihuTaskManager.taskQueue[0]
        ZhihuTaskManager.taskQueue = ZhihuTaskManager.taskQueue[1:]
        while tried < retry:
            if len(proxyList) == 0:
                afterNoProxyStrategy(True)
            proxy = proxyList[int(randNum() * len(proxyList))]
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
            ZhihuTaskManager.failedTask(task)
        if stopFlag():
            return
        if takebreak:
            time.sleep(21)
        time.sleep(int(randNum() * 3))
    pass


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
    ZhihuTaskManager.saveStatus()
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

class IdType:
    answer:str = 'answer'
    question:str = 'question'
    topic:str = 'topic'
    favorlist:str = 'favorlist'
    relatedquestion:str = 'relatedquestion'
    fullset = [answer,question,topic,favorlist,relatedquestion]

    @staticmethod
    def getType(qid: str):
        for tp in IdType.fullset:
            if qid.startswith(tp):
                return tp
        pass
    @staticmethod
    def convertId(type:str, id):
        return f'{type}_{id}'

    @staticmethod
    def convertAnswer(questionId:str, answerId:str):
        id = f'{questionId}_{answerId}'
        return IdType.convertId(IdType.answer,id)

    @staticmethod
    def stripId(rawId: str):
        return '_'.join(rawId.split('_')[1:])
    pass



def scrapeZhihu():
    def buildRequest(qid):
        # url = qid # targetUrl["detailprefix"].replace("[qid]", qid)
        header = {
            "User-Agent": requestConfig["user-agent"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cookie": "__snaker__id=kz4NFu3D5cvOrK21; _zap=a76ce729-4a8d-49d8-b447-8161ebfb0956; "
                      "d_c0=AFATjOukcRePTmL_1bARTis9Bys9xPP9QB0=|1695543525; "
                      "YD00517437729195%3AWM_TID=Ap6FvWBKH3lABVEUBQaF3KA8ZWcXHhIi; "
                      "_xsrf=ac5a7a98-ddd2-4381-9eb0-172a12528115; "
                      "Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1695543525,1695982812; "
                      "Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1696046093; "
                      "captcha_session_v2=2|1:0|10:1696046095|18:captcha_session_v2|88"
                      ":RllNY3UxVHdIZDB4WkZ0QWw0YTlXaGlRV1lrUi9POFEvMXlDb1JKcEdkV1Q2NVhEOHhjT2xtTFJnR0o4dEhmRw"
                      "==|1e96bd9adfdc41ace448856a95c8f7433bc3b10e831f4ab2be66cb408125b544; "
                      "YD00517437729195%3AWM_NI=G3FII7ntiLenx3tukd489q8oYi%2FzGhGvJNFHTOPVeRQo7Q1RaV6eS3w7Cv"
                      "%2FIu9NqKi8PnDke8iyiIbfijY0zy7zawqVTaFcvg1HdN9lAPWSIryFPa2H5Hzmlz%2F5qeERJMXk%3D; "
                      "YD00517437729195%3AWM_NIKE"
                      "=9ca17ae2e6ffcda170e2e6eea6ef4391ae8bb6e273b1ac8ba2c54a869e8ab0d43a90b698b6cc54b7aa9c92b82af0fea7c3b92a85ed8aaacc3daeaca7ade866bcedbc96ea70f8e8f792bb659bb7e19bc66485aa86afc5449891a0b7e85a93b1f9b2b45aa38afa86d239b5e98d97ae43b7e78292ca63fc90a2a5ea6ffcb7b78acc6aa6b7a6bab372bbe9b682f67b968cafa7e27ea5ef8885cd33b09fa0b8d243b2a78ab1e43a8ceb889bf068baf1fb92e84f929683b9ea37e2a3; gdxidpyhxdE=Vf6kflyVyHxDCM2HZ8ecws%2Bx2j9R4Dhbstofr%2Fr6E0C79xSJx%2FGeCDWNAp7sAOyijlH%5CcNtbX%2Fga5GRrdXoazMeqZP1kVGu1bUMIjoneiZGoCO%5CPTMGckuC141UV2iZtx%2FJNo6K%5C4P3OOgpU07o3wq1JcfvAoRCBi6aBTxv1fVLMiLHH%3A1696147794305; KLBRSID=76ae5fb4fba0f519d97e594f1cef9fab|1696146949|1696146881"
        }
        id = IdType.stripId(qid)
        if IdType.getType(qid) == IdType.answer:
            url = AnswerAnalyser.buildRequestURL(id)
            pass
        if IdType.getType(qid) == IdType.question:
            url = QuestionAnalyser.buildRequestURL(id)
            pass
        if IdType.getType(qid) == IdType.topic:
            url = TopicAnalyser.buildRequestURL(id)
            pass
        if IdType.getType(qid) == IdType.favorlist:
            url = FavorListAnalyser.buildRequestURL(id)
            pass
        if IdType.getType(qid) == IdType.relatedquestion:
            url = RelatedQuestionAnalyser.buildRequestURL(id)
        return url, header

    def recordAndDiscover(response, qid):
        dataStr = response.text
        if IdType.getType(qid) == IdType.answer:
            result = AnswerAnalyser.extractAndDiscover(dataStr)
            qTitle = result.titleText
            qContent = result.qContentText
            answer = result.answerText
            topics = result.topicIdList

            # new topics
            topicIds = [IdType.convertId(IdType.topic, topic) for topic in topics]
            for topicid in topicIds:
                ZhihuTaskManager.newTask(topicid)
            outputrow = qTitle + '\t' + qContent + '\t' + answer
            print(outputrow)
            record(outputrow)
        if IdType.getType(qid) == IdType.question:
            result = QuestionAnalyser.extractAndDiscover(dataStr)
            question = result.questionId
            for answer in result.answeridlist:
                answerId = IdType.convertAnswer(question, answer)
                ZhihuTaskManager.newTask(answerId)
            pass
        if IdType.getType(qid) == IdType.topic:
            pass
        if IdType.getType(qid) == IdType.favorlist:
            pass
        if IdType.getType(qid) == IdType.relatedquestion:
            pass
        # state saving
        ZhihuTaskManager.doneTask(qid)
        return False, True
    # stripedQueue = [q[-1] for q in qidQueue]
    scrapeGlobal(buildRequest, recordAndDiscover)
    ZhihuTaskManager.saveStatus()

def newQid(qid):
    if not scrapedQid.__contains__(qid) and not waitQid.__contains__(qid):
        waitQid.add(qid)
        taskQueue.append(qid)

def newTopic(topics):
    for topicId in topics:
        if not scrapedTopic.__contains__(topicId) and not waitingTopic.__contains__(topicId) and len(topicId) > 0:
            waitingTopic.add(topicId)
            taskQueue.append(topicId)

def newQuestion(question):
    pass

def newRelatedQuestion(question):
    pass

def newAnswer(question, answer):
    pass

def newFavorList(question):
    pass

def scrapeBossList():
    iter = 1
    retry = 3

    while iter < 200000:
        print(str(iter) + "/200000")
        tried = 0
        alldup = False
        while tried < retry:
            try:
                prox = proxyList[int(randNum() * len(proxyList))]
                response = requests.get(targetUrl["list"].replace("[page_index]", str(iter)), headers={"user-agent": requestConfig["user-agent"], "cookie": requestConfig["cookie"]})
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
        time.sleep(int(randNum() * 3))
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
    ZhihuTaskManager.loadStatus()
    # scrapeBossQuestionListByTopic()
    scrapeZhihu()
    # scrapeBossList()

if __name__ == '__main__':
    # waitingpath = os.path.abspath('../Resource/task/zhihu/waiting.txt')
    # list = CommonUtils.loadList(waitingpath)
    # for i in range(0, len(list)):
    #     list[i] = IdType.convertId(IdType.question, list[i])
    # CommonUtils.saveList(list,waitingpath)
    openf()
    main()
    closef()
