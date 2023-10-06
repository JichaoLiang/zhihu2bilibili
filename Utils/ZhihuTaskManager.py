from Utils.CommonUtils import CommonUtils
import os
class ZhihuTaskManager:
    dataBasePath = os.path.abspath('../Resource/task/zhihu/')

    waitingPath = os.path.join(dataBasePath, "waiting.txt")
    scrapedPath = os.path.join(dataBasePath, "scraped.txt")
    failedPath = os.path.join(dataBasePath, "failed.txt")

    taskQueue = []
    scrapedSet = set()
    failedSet = set()

    @staticmethod
    def loadStatus():
        ZhihuTaskManager.taskQueue = CommonUtils.loadList(ZhihuTaskManager.waitingPath)
        ZhihuTaskManager.scrapedSet = set(CommonUtils.loadList(ZhihuTaskManager.scrapedPath))
        ZhihuTaskManager.failedSet = set(CommonUtils.loadList(ZhihuTaskManager.failedPath))
        pass
    @staticmethod
    def loadScrapedAndFailed():
        ZhihuTaskManager.scrapedSet = set(CommonUtils.loadList(ZhihuTaskManager.scrapedPath))
        ZhihuTaskManager.failedSet = set(CommonUtils.loadList(ZhihuTaskManager.failedPath))
        pass

    @staticmethod
    def saveStatus():
        CommonUtils.saveList(ZhihuTaskManager.taskQueue, ZhihuTaskManager.waitingPath)
        CommonUtils.saveList(ZhihuTaskManager.scrapedSet, ZhihuTaskManager.scrapedPath)
        CommonUtils.saveList(ZhihuTaskManager.failedSet, ZhihuTaskManager.failedPath)

    @staticmethod
    def restoreScrapeDataQueue():
        list = [l.replace('\n', '') for l in CommonUtils.loadList(ZhihuTaskManager.waitingPath)]
        for l in list:
            ZhihuTaskManager.taskQueue.append(l)

        list = [l.replace('\n', '') for l in CommonUtils.loadList(ZhihuTaskManager.scrapedPath)]
        for l in list:
            ZhihuTaskManager.scrapedSet.add(l)

        list = [l.replace('\n', '') for l in CommonUtils.loadList(ZhihuTaskManager.failedPath)]
        for l in list:
            ZhihuTaskManager.failedSet.add(l)

    @staticmethod
    def newTask(id):
        if not ZhihuTaskManager.taskQueue.__contains__(id):
            ZhihuTaskManager.taskQueue.append(id)
        pass

    @staticmethod
    def newTaskImmediate(id):
        if ZhihuTaskManager.taskQueue.__contains__(id):
            ZhihuTaskManager.taskQueue.remove(id)
        ZhihuTaskManager.taskQueue = [id] + ZhihuTaskManager.taskQueue
        pass

    @staticmethod
    def failedTask(id):
        if ZhihuTaskManager.taskQueue.__contains__(id):
            ZhihuTaskManager.taskQueue.remove(id)
        if not ZhihuTaskManager.failedSet.__contains__(id):
            ZhihuTaskManager.failedSet.add(id)
        pass

    @staticmethod
    def doneTask(id):
        if ZhihuTaskManager.taskQueue.__contains__(id):
            ZhihuTaskManager.taskQueue.remove(id)
        if not ZhihuTaskManager.scrapedSet.__contains__(id):
            ZhihuTaskManager.scrapedSet.add(id)
        pass
    pass