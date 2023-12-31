from Utils.DBUtils import DBUtils


class Character:
    id = 0
    name = ''
    gender = 0
    voice = ''
    picgroupid = ''
    piclist = []

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
        instance.getPiclist()
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
        instance.getPiclist()
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
        instance.getPiclist()
        db.close()
        return instance

    def getPiclist(self):
        db = DBUtils()
        list = db.getPicListByCharacterId(self.id)
        db.close()
        piclist = [{
            "picgroupid": item[0],
            "path": item[1]
        } for item in list]
        self.piclist = piclist
        return piclist
        pass

