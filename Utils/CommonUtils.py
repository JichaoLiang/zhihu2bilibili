import os
import shutil
import time
from pathlib import Path
from random import random
from urllib.parse import urlencode

import bs4
from bs4 import ResultSet

import Config.Config


class CommonUtils:

    @staticmethod
    def urlencodestring(string: str):
        data = urlencode({'aaa': string})
        return '='.join(data.split('=')[1:])

    @staticmethod
    def now_short_string():
        localtime = time.localtime(time.time())
        return time.strftime('%Y-%m-%d', localtime)

    @staticmethod
    def tryFetch(jsonelement, attrlist: list):
        pointer = jsonelement
        for i in range(0, len(attrlist)):
            attr = attrlist[i]
            if pointer is None or len(pointer) == 0:
                return ''
            pointer = pointer[attr]
        return pointer
        pass

    @staticmethod
    def tryFetchHtml(htmlElement, selectCommandList: list):
        pointer = htmlElement
        for i in range(0, len(selectCommandList)):
            comm = selectCommandList[i]
            if pointer is None or len(pointer) == 0:
                return ''
            obj: ResultSet = ResultSet(source=None)
            if type(pointer) == type(obj):
                pointer = pointer[0]
            pointer = pointer.select(comm)
        return pointer
        pass

    @staticmethod
    def htmlToText(p):
        tokens = []
        while p.__contains__('<') or p.__contains__('>'):
            tks = p.split('<')
            tokens.append(tks[0])
            p = '<'.join(tks[1:])
            tks = p.split('>')
            p = '>'.join(tks[1:])
        tokens.append(p)

        return ''.join(tokens).replace('\n', '').replace('\t', '')
        pass

    @staticmethod
    def readAllText(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                list = f.read()
                # print(list)
                return list
        except Exception as ex:
            print(ex)
            return ""

    @staticmethod
    def writeAllText(path, datastring):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(datastring)
                # print(list)
        except Exception as ex:
            print(ex)

    @staticmethod
    def loadList(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                list = f.readlines()
                for i in range(0, len(list)):
                    if list[i].endswith('\n'):
                        list[i] = list[i][0:-1]
                return list
        except Exception as ex:
            return []

    @staticmethod
    def saveList(list, path):
        file = Path(path)
        if file.exists():
            os.remove(path)
        with open(path, 'w', encoding='utf-8') as writer:
            for line in list:
                writer.write(line + "\n")
        pass

    @staticmethod
    def cleanList(path):
        data = CommonUtils.loadList(path)
        for i in range(0, len(data)):
            line = data[i]
            if line.__contains__('/'):
                data[i] = line.split('/')[-1]
        CommonUtils.saveList(data, path)

    @staticmethod
    def random01() -> float:
        rand = random.Random()
        return rand.random()

    pass


class UrlType():
    topic = 'topic'
    question = 'question'
    answer = 'answer'
    favorlist = 'favorlist'

    questionUrlKeyword = 'www.zhihu.com/question/'

    @staticmethod
    def getUrlType(url: str) -> str:
        if False:
            return UrlType.topic
        if False:
            return UrlType.question
        if url.lower().__contains__(UrlType.questionUrlKeyword) and url.lower().__contains__('answer'):
            return UrlType.answer
        if False:
            return UrlType.favorlist
        pass

    pass


if __name__ == '__main__':
    CommonUtils.readAllText(Config.Config.Config.bilibiliCredentialPath)
