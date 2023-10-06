import os
import time

from Config.Config import Config


class DataStorageUtils:
    @staticmethod
    def generatePathId(extName, namespacefolder):
        fnow = time.time()
        intNow = int(fnow * 1000)
        milliSec = intNow % 1000
        now = time.localtime(fnow)
        id = f'{now.tm_year}_{now.tm_mon}_{now.tm_mday}_{now.tm_hour}_{now.tm_min}_{now.tm_sec}_{milliSec}.{extName}'
        destPath = os.path.join(Config.dataPath,f'{namespacefolder}/{now.tm_year}_{now.tm_mon}/{now.tm_mday}/{id}')
        return id,  destPath

    @staticmethod
    def generatePicPathId(extName = 'jpg'):
        return DataStorageUtils.generatePathId(extName,'PicData')
        pass

    @staticmethod
    def pathById(picId: str)->str:
        tokens = picId.split('_')
        year = tokens[0]
        mon = tokens[1]
        day = tokens[2]
        hour = tokens[3]
        min = tokens[4]
        sec = tokens[5]
        millisec = tokens[6]

        destPath = os.path.join(Config.dataPath,f'PicData/{year}_{mon}/{day}/{picId}')
        return destPath
        pass
    pass