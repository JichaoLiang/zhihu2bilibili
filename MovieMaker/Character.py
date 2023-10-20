from random import Random

from Utils.DBUtils import DBUtils
from Utils.DataStorageUtils import DataStorageUtils


class Character:
    id = 0
    name = ''
    gender = 0
    voice = ''
    picgroupid = ''
    videogroupid = ''
    piclist = []
    videolist = []

    def randomVideoByTag(self, tag:list):
        tagged = [v for v in self.videolist if tag.__contains__(v['tag'])]
        picked = Random().choice(tagged)
        id = picked['path']
        filepath = DataStorageUtils.moviePathById(id)
        return filepath

    def randomPicByTag(self, tag:list):
        tagged = [v for v in self.piclist if tag.__contains__(v['tag'])]
        picked = Random().choice(tagged)
        id = picked['path']
        filepath = DataStorageUtils.picPathById(id)
        return filepath

    @staticmethod
    def fromId(id):
        db = DBUtils()
        randCharacter = db.characterById(id)
        instance = Character()
        instance.id = randCharacter[0]
        instance.name = randCharacter[1]
        instance.gender = randCharacter[2]
        instance.voice = randCharacter[3]
        instance.picgroupid = randCharacter[4]
        instance.videogroupid = randCharacter[5]
        instance.getPiclist()
        instance.getVideoList()
        db.close()
        return instance

    @staticmethod
    def randomCharacter():
        db = DBUtils()
        randCharacter = db.randomCharacter()
        instance = Character()
        instance.id = randCharacter[0]
        instance.name = randCharacter[1]
        instance.gender = randCharacter[2]
        instance.voice = randCharacter[3]
        instance.picgroupid = randCharacter[4]
        instance.videogroupid = randCharacter[5]
        instance.getPiclist()
        instance.getVideoList()
        db.close()
        return instance

    @staticmethod
    def randomMale():
        db = DBUtils()
        randCharacter = db.randomMale()
        instance = Character()
        instance.id = randCharacter[0]
        instance.name = randCharacter[1]
        instance.gender = randCharacter[2]
        instance.voice = randCharacter[3]
        instance.picgroupid = randCharacter[4]
        instance.videogroupid = randCharacter[5]
        instance.getPiclist()
        instance.getVideoList()
        db.close()
        return instance

    @staticmethod
    def randomFemale():
        db = DBUtils()
        randCharacter = db.randomFemale()
        instance = Character()
        instance.id = randCharacter[0]
        instance.name = randCharacter[1]
        instance.gender = randCharacter[2]
        instance.voice = randCharacter[3]
        instance.picgroupid = randCharacter[4]
        instance.videogroupid = randCharacter[5]
        instance.getPiclist()
        instance.getVideoList()
        db.close()
        return instance

    def getPiclist(self):
        db = DBUtils()
        list = db.getPicListByCharacterId(self.id)
        db.close()
        piclist = [{
            "picgroupid": item[0],
            "path": item[1],
            "tag": item[2]
        } for item in list]
        self.piclist = piclist
        return piclist
        pass

    def getVideoList(self):
        db = DBUtils()
        list = db.getVideoListByCharacterId(self.id)
        db.close()
        videolist = [{
            "videogroupid": item[0],
            "path": item[1],
            "tag": item[2]
        } for item in list]
        self.videolist = videolist
        return videolist
        pass

