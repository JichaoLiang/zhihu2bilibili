import random
from importlib import reload

from bs4 import BeautifulSoup
import requests
import json
import time

import TutorialDemo
# import randomNum
import io
import os.path
from pathlib import Path
import traceback
# import urllib.parse
import urllib
import re
import sys
import Scraper.Analyser
from Config.Config import Config
from Scraper.Analyser.BingSearchAnalyser import BingSearchAnalyser
from Scraper.Analyser.QuestionAnalyser import QuestionAnalyser
from Scraper.Analyser.AnswerAnalyser import AnswerAnalyser
from Scraper.Analyser.RelatedQuestionAnalyser import RelatedQuestionAnalyser
from Scraper.Analyser.FavorListAnalyser import FavorListAnalyser
from Scraper.Analyser.SearchKeywordAnalyser import SearchKeywordAnalyser
from Scraper.Analyser.TopicAnalyser import TopicAnalyser
from Scraper.Enums.QuestionDomain import QuestionDomain
from Utils.CommonUtils import CommonUtils
from Utils.DBUtils import DBUtils
from Utils.ZhihuTaskManager import ZhihuTaskManager
from Scraper.Enums.IdType import IdType

#
# reload(sys)
# sys.setdefaultencoding('utf-8')

requestConfig = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "cookie": "MUID=3B94E3408A8C6F0A0A4CF1348B976E27; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=F8268E82B39849A7931EC5F7F56E05DF&dmnchg=1; MUIDB=3B94E3408A8C6F0A0A4CF1348B976E27; MicrosoftApplicationsTelemetryDeviceId=4683975d-c6fe-44a0-bd1b-ae5bf48f7873; PPLState=1; SnrOvr=X=rebateson; MMCASM=ID=E0F9DB97F5744A70AD7270B1E638C941; ANON=A=32A5624CED8D971858B5FD7FFFFFFFFF&E=1c80&W=1; _UR=QS=0&TQS=0&cdxcls=0; NAP=V=1.9&E=1c8e&C=gzwiKvBOEPeOW4Wj4266WaIcHTLVA3cDmtiD-7hcaRKgKLJCblCtFA&W=1; KievRPSSecAuth=FAByBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACPVUHhwLDv4HMAQ6ScRGqdTLSzIRdxQHogDlx1dTjnOqKXK5OBNTp14TSCHGO5xM5AsMvx+fcCswPI99vKa0Uc56/07Wvh5Ucy7qbegOUNCJIrZTCAOd0DqhNUsIe5powF88MEJyO3oefvPEWyYXVVSf2S2CIz2TWWF8b9+suvmwBjWPs0HJS9bdVAS98liIes0iH++D+LlUxkvGmIpr0oJQRUDiFmmZArC4Q3nkVzRawkfZna8jJupYkF2rweEAns1UUSQO2aUFDbPSvFGBRf/g1w26J960QC2rN5tljOnI2sMKbpyJWxxLPFCTAm2GqW1D7cXfUFxdfMt2Z1e6IF7mqBACvQLvvuuOr0zgEVB72tmSM5zddRichwIxf7EeoXHxZ2ZhEQSC9PHeecY32fLCOmLBgr0MyKlkDUzUJku6WqzxktZenqxKUz5sRDl7gkmi/TL8utIReIix+vCseXS/V0MSjdO8X2XwaryreLmibYGkyqqGJti8eKgYHiUZ3iyKsdsYvVm56nWuftsalrMYyfZtUNxiBBgDkUyP0OS//LJKWQzK4YqaBseGABHWVdfzS13WFfyyuCcYlUpYvJnbJlaYRUG9TU+mWlEsPuZoZhsmis6gEM17qUH7DonPW0psAyG0+GJa8jurNpSZ6MiDDY02kARMM9lmJRc7kHKlJmLECeNkD8oTn9QL+fzMEdU9Wk2djfpaj0XROJtJzAzH7cUq/v0nacZYbN2sx4YqXQKrMfNJCbdydC67R37t5Cgg0luiF99eCileIFuV1ZWHv2T0LRz0HJNfDhC9mXg4qptxbUjimAUr76KnmB3OJTAZgtHhUrBfpiJZpsz6z4OuefsKpkZyHrdbGrtr98CQFfKYX/60sv0vrZyfD/qM0lps2maWTaPVsbBWFnDqBmThrNjKEZQfl84fwv+wjvv9jIvNHs+e1t7Qeh0PBNvJOFLF64zqf5T1F2xDstUVYawkwTvhLb506Dt/GDYPnz0rdQV5JE3ZJ+L1i+1+3Uni/3KE3JS4puiRpBJh462WR/ewpQ780h5hQeBdeDtQW4UXUzsn1kAp33ogACc/ghI6316djISoHkxTOyTJ/lDBz6bzfrSGVIOf6eMexq9Qh0a2/R5b0cOQ3Zr/3LmksJlMN8ii88yIDckB5l2JPAexeLNbIf96WQoXFKumoxotzWiiQ8ADPWip8Rfvaq3asI6/LYSaktIdIQqkZhXcBcDt+MLtKbKV+t933FJWg1dA+rLlUVCrlf7FuUbI/WkJU2IUwVMwq0NBZ8mSZXDXWCY24rr8nHmxdO3A6v7ZiQebPS96BDXLxTIEDT0Q9G16S7Bo5shPMbozIC0ZA31jxuAF0zwv2Uzf7jMpP+3xXQhZGPzMPMtJbb84Nm8K6+1123wl2pLMvLdNavRITMAkCp4zpMpu7j5dqm3BeG6YFACs/2/Y3g0KzJWbhALv+PBn55aVKw==; MSCCSC=1; _HPVN=CS=eyJQbiI6eyJDbiI6MTcsIlN0IjowLCJRcyI6MCwiUHJvZCI6IlAifSwiU2MiOnsiQ24iOjE3LCJTdCI6MCwiUXMiOjAsIlByb2QiOiJIIn0sIlF6Ijp7IkNuIjoxNywiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0xMS0yMVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjo2MSwiVG9iYnMiOjB9; ipv6=hit=1700571129835&t=4; _Rwho=u=d; ai_session=KzAUSY73GtHk7bq4dzJFmZ|1700567531095|1700567531095; USRLOC=HS=1&ELOC=LAT=39.96904373168945|LON=116.48928833007812|N=%E6%9C%9D%E9%98%B3%E5%8C%BA%EF%BC%8C%E5%8C%97%E4%BA%AC%E5%B8%82|ELT=6|; SRCHUSR=DOB=20221208&T=1700567529000&TPC=1700567542000; _SS=SID=28E3F85EECAF69DA09E6EB8EEDE5684E&R=441&RB=441&GB=0&RG=0&RP=441; _RwBf=ilt=23&ihpd=1&ispd=0&rc=441&rb=441&gb=0&rg=0&pc=441&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=5&l=2023-11-21T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=BINGCOPILOTWAITLIST&c=MR000T&t=3146&s=2023-05-13T06:41:56.6719363+00:00&ts=2023-11-21T11:55:36.9008507+00:00&rwred=0&wls=2&lka=0&lkt=0&TH=&r=1&mta=0&e=CDH4m6z6z-vKniIU_F76f-3kF9tgmYpNo3650x5qDBhq-_K1Glz1SyAhJRdnT8bq6I-T99K4O3wkpz_Yw59kdl5TAMFxIMiH90YY18IfjE8&A=&dci=0&wlb=0&aad=0; SRCHHPGUSR=SRCHLANG=zh-Hans&BRW=XW&BRH=T&CW=2560&CH=1291&SCW=2543&SCH=3274&DPR=1.0&UTC=480&DM=0&WTS=63836164329&HV=1700567737&PRVCW=662&PRVCH=1291&PV=10.0.0&BZA=0&IG=4C4C58128620429A8BE425BB2EA2C81D&EXLTT=2&CIBV=1.1342.2; _EDGE_S=SID=28E3F85EECAF69DA09E6EB8EEDE5684E&mkt=zh-cn"
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

proxyVoteDict = {

}

for i in range(0, len(proxyList)):
    proxyVoteDict.setdefault(proxyList[i]["http"], 0)

index = 0
maxLine = 10000

database = DBUtils()

handler = None
lineCount = 0

qSet = set()
duplicated = 0

#
# qidQueue = []
# topicQueue = []


dataBasePath = os.path.join(Config.basePath, 'Resource/task/zhihu/')
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
    global lineCount, index, handler, target
    pth = target + "_" + str(index) + ".txt"
    if not Path(pth).exists():
        open(Path(pth), 'x', encoding='utf-8').close()
    handler = open(target + "_" + str(index) + ".txt", 'a', encoding='utf-8')
    index += 1
    lineCount = 0


def closef():
    global handler
    handler.close()


def record(msg):
    global handler, lineCount
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

        for i in range(0, len(builderlist)):
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
        time.sleep(int(randNum() * 8))
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


def topicInfoToDict(topicId, topicName, qCount, fCount):
    if topicInfoDict.get(topicId) == None:
        topicInfoDict.setdefault(topicId, [topicName, qCount, fCount])


def saveTopicInfo():
    with open(topicInfoPath, 'a') as f:
        for k in topicInfoDict.keys():
            val = topicInfoDict.get(k)
            f.write(k + "\t" + val[0] + "\t" + str(val[1]) + "\t" + str(val[2]) + "\n")


def convertNewLineAndTable(str):
    return str.replace('\n', '<br />').replace('\t', '&nbsp;')


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


def checkAndInsertDB(answerId, result, scenario='default'):
    qTitle = result.titleText
    qContent = result.qContentText
    answer = result.answerText
    topics = result.topicIdList
    topicname = result.topics
    voteCount = result.voteCount
    commentCount = result.commentCount
    updated = result.updated
    isCollapsed = result.isCollapsed
    questionid = answerId.split('_')[1]

    decision = AnswerAnalyser.dataPickStrategy(result)
    if decision != 'ok':
        print(f'answer {answerId} will not be inserted into db due to reason: {decision}')
        print(decision)
        return
    exists = database.answerExists(answerId)
    if not exists:
        database.newAnswer(answerId, qTitle, qContent, answer, updated, topicname, topics, voteCount, commentCount,
                           scenario, isCollapsed, questionid)
    pass


def scrapeZhihu(tagmark):
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
        if IdType.getType(qid) == IdType.search:
            url, header = SearchKeywordAnalyser.buildRequestURL(id, header)
        if IdType.getType(qid) == IdType.bingsearch:
            url, header = BingSearchAnalyser.buildRequestURL(id)
        return url, header

    def recordAndDiscover(response, qid):
        dataStr = response.text
        if IdType.getType(qid) == IdType.answer:
            result = AnswerAnalyser.extractAndDiscover(dataStr, qid)
            qTitle = result.titleText
            qContent = result.qContentText
            answer = result.answerText
            topics = result.topicIdList
            topicname = result.topics
            voteCount = result.voteCount
            commentCount = result.commentCount
            updated = result.updated
            isCollapsed = result.isCollapsed

            # new topics
            topicIds = [IdType.convertId(IdType.topic, topic)[0] for topic in topics]
            for topicid in topicIds:
                ZhihuTaskManager.newTask(topicid)
            outputrow = qTitle + '\t' + qContent + '\t' + answer
            print(outputrow)
            record(outputrow)
            checkAndInsertDB(qid, result, tagmark)
        if IdType.getType(qid) == IdType.question:
            result = QuestionAnalyser.extractAndDiscover(dataStr, qid)
            question = result.questionId
            for answer in result.answeridlist:
                answerId = IdType.convertAnswer(question, answer)
                ZhihuTaskManager.newTaskImmediate(answerId)
            sessionid = result.sessionid
            lastcursor = result.lastcursor
            batch = result.batch
            if batch >= 0:
                taskId = IdType.convertQuestion(question, batch, lastcursor, sessionid)
                ZhihuTaskManager.newTaskImmediate(taskId)
            pass
        if IdType.getType(qid) == IdType.topic:
            pass
        if IdType.getType(qid) == IdType.favorlist:
            pass
        if IdType.getType(qid) == IdType.relatedquestion:
            pass
        if IdType.getType(qid) == IdType.bingsearch:
            result = BingSearchAnalyser.extractAndDiscover(dataStr)
            qnaList = result.qnaPairList
            for qnaPair in qnaList:
                questionId = qnaPair
                questionTaskId = IdType.convertQuestion(questionId, -1, '', '')
                ZhihuTaskManager.newTaskImmediate(questionTaskId)
            pass
        if IdType.getType(qid) == IdType.search:
            result = SearchKeywordAnalyser.extractAndDiscover(dataStr, qid)
            qnalist = result.idlist
            for qna in qnalist:
                answer = qna[0]
                question = qna[1]
                questionjobid = IdType.convertQuestion(question, -1, '', '')
                ZhihuTaskManager.newTask(questionjobid)
                pass
        # state saving
        ZhihuTaskManager.doneTask(qid)
        return False, True

    # stripedQueue = [q[-1] for q in qidQueue]
    scrapeGlobal(buildRequest, recordAndDiscover)
    database.close()
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
                response = requests.get(targetUrl["list"].replace("[page_index]", str(iter)),
                                        headers={"user-agent": requestConfig["user-agent"],
                                                 "cookie": requestConfig["cookie"]})
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
                    qUrl = targetUrl["detailprefix"].replace("[qid]",
                                                             str(item["questionInfo"]["linkUrl"]).split("questionId=")[
                                                                 -1].split("&")[0])
                    answerCount = item["questionInfo"]["answerCount"]
                    topic = item["topicName"]
                    if qSet.__contains__(question):
                        global duplicated
                        duplicated += 1
                        dupCount += 1
                        print("dup: " + str(duplicated))
                    else:
                        qSet.add(question)
                        record(question + "\t" + qUrl + "\t" + str(answerCount) + "\t" + topic)
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
                            seedDict.add(id + "\t" + siteUrl)
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
    saveList(list(seedDict), seedOutputPath)
    pass


def main():
    # scrapeSeedUrlBykey()
    ZhihuTaskManager.loadStatus()
    # scrapeBossQuestionListByTopic()
    scrapeZhihu()
    # scrapeBossList()


# period = week / day / hour
def scrapeRoutineJob(topicIdList, tagmark='hottopic', period='day'):
    ZhihuTaskManager.loadScrapedAndFailed()
    for topic in topicIdList:
        result = TutorialDemo.run(topic, period)
        questionIdList = [IdType.convertId(IdType.question, row[2]) for row in result]
        for qid in questionIdList:
            ZhihuTaskManager.taskQueue += qid
    print(f'question list generated, {len(ZhihuTaskManager.taskQueue)} total.')
    scrapeZhihu(tagmark)


def scrapeKeywords(keywords: list, tagmark='search'):
    ZhihuTaskManager.loadScrapedAndFailed()
    for keyword in keywords:
        taskId = IdType.convertId(IdType.search, keyword)[0]
        ZhihuTaskManager.taskQueue.append(taskId)
        print(f'task generated: id={taskId}')
    if tagmark == 'search':
        tagmark = f'search_{",".join(keywords)}_{CommonUtils.now_short_string()}'
    scrapeZhihu(tagmark)
    pass


def scrapeBaiduKeywords(keywords: list, tagmark='bingsearch'):
    ZhihuTaskManager.loadScrapedAndFailed()
    for keyword in keywords:
        taskId = IdType.convertId(IdType.bingsearch, keyword)[0]
        ZhihuTaskManager.taskQueue.append(taskId)
        print(f'task generated: id={taskId}')
    if tagmark == 'bingsearch':
        tagmark = f'bingsearch_{keywords[0]}_{CommonUtils.now_short_string()}'
    scrapeZhihu(tagmark)


def processSearchList():
    openf()
    scrapeBaiduKeywords(['缅北电诈', '楼市'])
    closef()


def processSearchKeywords(list: list, tagmark='bingsearchkeyword'):
    openf()
    scrapeBaiduKeywords(list, tagmark)
    closef()


def process():
    openf()
    topicIdList = [
        # QuestionDomain.dongmanyouxi,
        QuestionDomain.dongmanyouxi,
        QuestionDomain.shuma
        # QuestionDomain.muyingqinzi,
        # QuestionDomain.qinggan
    ]
    tagmark = '_'.join([str(item) for item in topicIdList]) + "_" + CommonUtils.now_short_string()
    scrapeRoutineJob(topicIdList, tagmark, period='day')
    closef()


if __name__ == '__main__':
    process()
    # processSearchList()
