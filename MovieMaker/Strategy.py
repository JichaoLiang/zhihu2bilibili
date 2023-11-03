import random
from random import Random

from Config.Config import Config
from MovieMaker.Character import Character
from Utils.DBUtils import DBUtils
from Utils.DataStorageUtils import DataStorageUtils


class Strategy:
    # 三个actor的顺序
    @staticmethod
    def getSpeechActorIdList():
        presidents = [19, 20, 21]
        result = []
        while len(presidents) > 0:
            picked = Random().choice(presidents)
            result.append(picked)
            presidents.remove(picked)
        return result
        pass
    # 主持人id
    @staticmethod
    def getSpeechHostCharacterId():
        return Character.randomMale().id
        pass

    @staticmethod
    def getBGMFile():
        db = DBUtils()
        bgmrows = [row[4] for row in db.getVoiceByTag('bgm')]
        return DataStorageUtils.voicePathById(random.Random().choice(bgmrows))

    @staticmethod
    def getEndScenario():
        db = DBUtils()
        endrows = [row[3] for row in db.getVideoListByTag('end')]
        return DataStorageUtils.moviePathById(random.Random().choice(endrows))
    # 回答过滤器
    @staticmethod
    def filterAnswer(answer):
        longenough = Config.minAnswerLength < len(answer) < Config.maxAnswerlength
        wordblacklist = []
        return longenough
        pass


if __name__ == '__main__':
    print(Strategy.getEndScenario())

