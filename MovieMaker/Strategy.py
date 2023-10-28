from random import Random

from MovieMaker.Character import Character


class Strategy:
    # 三个actor的顺序
    @staticmethod
    def getSpeechActorIdList():
        presidents = [13, 14, 15]
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
    def getLeaderVideoIndex(characterid):
        character = Character.fromId(characterid)
        if character.name == 'obama':
            return 2
        if character.name == 'putin':
            return 2
        if character.name == 'trump':
            return 1
        return -1
        pass

    @staticmethod
    def getEndScenario():
        trump = Character.fromId(15)
        endvideopath = trump.randomVideoByTag(['end'])
        return endvideopath
        pass

