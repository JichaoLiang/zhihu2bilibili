import os.path
import time
from pathlib import Path
import shutil
import MovieMaker.TTS
import uuid

from Config.Config import Config
from Utils.CommonUtils import CommonUtils
from Utils.DBUtils import DBUtils
from Utils.DataStorageUtils import DataStorageUtils


class BackendManagement:
    @staticmethod
    def newCharacterFromDirectory(dataDirPath: str):
        pathName = os.path.basename(dataDirPath)
        tokens = pathName.split('_')
        name = tokens[0]
        isMale = 1
        if len(tokens) > 1 and tokens[1].lower() != 'male':
            isMale = 0
        if isMale:
            voice = Config.voice_male_default
            pass
        else:
            voice = Config.voice_female_default
            pass
        if len(tokens) > 2:
            voice = tokens[2]
        picGroupId = uuid.uuid1()

        files = os.listdir(dataDirPath)
        files = [os.path.join(dataDirPath, f) for f in files]
        picinfolist = []
        for file in files:
            filePath = Path(file)
            if filePath.is_file():
                baseName = os.path.basename(file)
                fileName = baseName.split('.')[0].lower()
                extendName = baseName.split('.')[-1].lower()
                if extendName in ['jpg', 'jpeg', 'png']:
                    nameInfoTokens = fileName.split('_')
                    picindex = int(nameInfoTokens[0])
                    if len(nameInfoTokens) > 1:
                        tag = nameInfoTokens[1]
                    else:
                        tag = ''
                    id, destPath = DataStorageUtils.generatePicPathId(extendName)
                    destDir = os.path.dirname(destPath)
                    if not Path(destDir).exists():
                        os.makedirs(destDir)
                    shutil.copyfile(filePath, destPath)
                    picdata = (picGroupId, picindex, id, tag)
                    picinfolist.append(picdata)

        db = DBUtils()
        db.newCharacter(name, isMale, voice, picinfolist)
        db.close()
        pass
    @staticmethod
    def indexfolder(folderpath):
        files = os.listdir(folderpath)
        fullpath = [os.path.join(folderpath, f) for f in files]
        for i in range(0, len(fullpath)):
            file = fullpath[i]
            extendName = os.path.basename(file).split('.')[-1]
            destFile = os.path.join(folderpath, f'{i+1}.{extendName}')
            if Path(file).is_file():
                shutil.move(file,destFile)

    @staticmethod
    def test():
        folderpath = 'G:\\import\\randomgirl_female'
        # convert files in folder from 1 to n, if the character booked manually, do not call this which will mess up the order
        BackendManagement.indexfolder(folderpath)
        BackendManagement.newCharacterFromDirectory(folderpath)
        pass
    pass

if __name__ == '__main__':
    BackendManagement.test()