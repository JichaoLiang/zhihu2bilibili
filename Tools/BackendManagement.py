import os.path
import time
from pathlib import Path
import shutil
import MovieMaker.TTS
import uuid

from Config.Config import Config
from Config.VoiceModel import VoiceModel
from Scraper.Enums.Status import taskStatus, qnaStatus
from Utils.BaidunetdiskUtils import BaidunetdiskUtils
from Utils.CommonUtils import CommonUtils
from Utils.DBUtils import DBUtils
from Utils.DataStorageUtils import DataStorageUtils


class BackendManagement:
    @staticmethod
    def newVideoCharacterFromDirectory(dataDirPath: str):
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
        videoGroupId = uuid.uuid1()

        files = os.listdir(dataDirPath)
        files = [os.path.join(dataDirPath, f) for f in files]
        picinfolist = []
        for file in files:
            filePath = Path(file)
            if filePath.is_file():
                baseName = os.path.basename(file)
                fileName = baseName.split('.')[0].lower()
                extendName = baseName.split('.')[-1].lower()
                if extendName in ['mp4']:
                    nameInfoTokens = fileName.split('_')
                    picindex = int(nameInfoTokens[0])
                    if len(nameInfoTokens) > 1:
                        tag = nameInfoTokens[1]
                    else:
                        tag = ''
                    id, destPath = DataStorageUtils.generateMoviePathId(extendName)
                    destDir = os.path.dirname(destPath)
                    if not Path(destDir).exists():
                        os.makedirs(destDir)
                    shutil.copyfile(filePath, destPath)
                    picdata = (videoGroupId, picindex, id, tag)
                    picinfolist.append(picdata)

        db = DBUtils()
        db.newCharacter(name, isMale, voice, picinfolist)
        db.close()
        pass

    @staticmethod
    def newBGM(filpath):
        BackendManagement.newVoice(filpath, tag="bgm")

    @staticmethod
    def newVoice(filepath, name=None, specifiedgroupid=None, tag=''):
        extName = filepath.split('.')[-1]
        id, destPath = DataStorageUtils.generateVoicePathId(extName)
        shutil.copyfile(filepath, destPath)

        groupid = specifiedgroupid

        if name is None:
            name = str(os.path.basename(filepath)).split('.')[0]

        if specifiedgroupid is None:
            groupid = uuid.uuid1()
        # single mode
        index = 0
        db = DBUtils()
        db.newAudio(name, groupid, index, id, tag)
        pass

    @staticmethod
    def newCharacterFromDirectory(dataDirPath: str):
        pathName = os.path.basename(dataDirPath)
        tokens = pathName.split('_')
        name = tokens[0]
        isMale = 1
        if len(tokens) > 1 and tokens[1].lower() != 'male':
            isMale = 0
        if isMale:
            voice = VoiceModel.default_male['ShortName']  # Config.voice_male_default
            pass
        else:
            voice = VoiceModel.default_female['ShortName']  # Config.voice_female_default
            pass
        if len(tokens) > 2:
            voice = tokens[2]
        picGroupId = uuid.uuid1()
        videoGroupId = uuid.uuid1()

        files = os.listdir(dataDirPath)
        files = [os.path.join(dataDirPath, f) for f in files]
        picinfolist = []
        videoinfolist = []
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
                elif extendName in ['mp4']:
                    nameInfoTokens = fileName.split('_')
                    videoindex = int(nameInfoTokens[0])
                    if len(nameInfoTokens) > 1:
                        tag = nameInfoTokens[1]
                    else:
                        tag = ''
                    id, destPath = DataStorageUtils.generateMoviePathId(extendName)
                    destDir = os.path.dirname(destPath)
                    if not Path(destDir).exists():
                        os.makedirs(destDir)
                    shutil.copyfile(filePath, destPath)
                    videodata = (videoGroupId, videoindex, id, tag)
                    videoinfolist.append(videodata)

        db = DBUtils()
        db.newCharacter(name, isMale, voice, picinfolist, videoinfolist)
        db.close()
        pass

    @staticmethod
    def indexfolder(folderpath):
        files = os.listdir(folderpath)
        fullpath = [os.path.join(folderpath, f) for f in files]
        for i in range(0, len(fullpath)):
            file = fullpath[i]
            extendName = os.path.basename(file).split('.')[-1]
            destFile = os.path.join(folderpath, f'{i + 1}.{extendName}')
            if Path(file).is_file():
                shutil.move(file, destFile)

    @staticmethod
    def generatequestionidbatch():
        db = DBUtils()
        answers = db.doQuery('select idqna, answerid from zhihu2bilibili.qna;')
        for answer in answers:
            idqna = answer[0]
            answerid = answer[1]
            questionid = answerid.split('_')[1]
            db.doCommand(f'update zhihu2bilibili.qna set questionid="{questionid}" where idqna="{idqna}";')
        db.close()
        pass

    @staticmethod
    def clearQnaStatusByTask():
        db = DBUtils()
        questionids = db.doQuery('select distinct(questionid) from zhihu2bilibili.taskstatus')
        db.doCommand(f'update  zhihu2bilibili.qna set taskgenerated={qnaStatus.notStarted} where 1=1;')
        for q in questionids:
            questionid = q[0]
            db.doCommand(
                f'update zhihu2bilibili.qna set taskgenerated={qnaStatus.complete} where questionid="{questionid}";')

    @staticmethod
    def clearTTSJobByTask():
        db = DBUtils()
        taskids = db.doQuery(
            'select distinct(idtaskstatus) from zhihu2bilibili.taskstatus where ttssuccess = 2 and charactersuccess=0')
        # db.doCommand(f'update  zhihu2bilibili.qna set taskgenerated={qnaStatus.notStarted} where 1=1;')
        for task in taskids:
            t = task[0]
            db.doCommand(f'delete from zhihu2bilibili.ttstask where taskid="{t}";')

    # 根据taskid范围抹除生产痕迹=.=
    @staticmethod
    def eraseJobByTaskId(min, max):
        db = DBUtils()
        questionids = db.doQuery(
            f'select idtaskstatus,questionid from zhihu2bilibili.taskstatus where idtaskstatus < {max} and idtaskstatus > {min}')
        for q in questionids:
            questionid = q[1]
            taskid = q[0]
            db.doCommand(
                f'update zhihu2bilibili.qna set taskgenerated={qnaStatus.notStarted} where questionid="{questionid}";')
            db.doCommand(f'delete from zhihu2bilibili.ttstask where taskid="{taskid}";')
            db.doCommand(f'delete from zhihu2bilibili.videochunk where taskstatusid="{taskid}";')
        db.doCommand(f'delete from zhihu2bilibili.taskstatus where idtaskstatus < {max} and idtaskstatus > {min}')
        db.close()

    @staticmethod
    def addVideoToCharacter(videoPath, characterName, tag):
        db = DBUtils()
        id, path = DataStorageUtils.generateMoviePathId()
        shutil.copyfile(videoPath, path)
        sql = f'SELECT videogroupid FROM zhihu2bilibili.character where name="{characterName}"'
        videogroupid = db.doQuery(sql)[0][0]
        sql = f'SELECT max(IndexInGroup) FROM zhihu2bilibili.videoresourcedata where VideoGroupId="{videogroupid}"'
        maxIndex = db.doQuery(sql)[0][0]
        sql = f'insert into zhihu2bilibili.videoresourcedata(VideoGroupId,IndexInGroup,RelPath,Tag) ' \
              f'values("{videogroupid}","{str(maxIndex + 1)}","{id}","{tag}")'
        db.doCommand(sql)
        db.close()
        pass

    @staticmethod
    def removeVideoToCharacter(characterName, indexId):
        db = DBUtils()
        sql = f'SELECT videogroupid FROM zhihu2bilibili.character where name="{characterName}"'
        videogroupid = db.doQuery(sql)[0][0]
        sql = f'delete from zhihu2bilibili.videoresourcedata where VideoGroupId="{videogroupid}" and IndexInGroup="{indexId}"'
        db.doCommand(sql)
        db.close()
        pass

    @staticmethod
    def test():
        folderpath = 'H:/character_import/trump_male'
        # convert files in folder from 1 to n, if the character booked manually, do not call this which will mess up the order
        # BackendManagement.indexfolder(folderpath)
        BackendManagement.newCharacterFromDirectory(folderpath)
        pass

    pass


if __name__ == '__main__':
    BackendManagement.eraseJobByTaskId(6847, 99999)
    # BackendManagement.removeVideoToCharacter('putin', 5)
    # path = r'Q:\baiduNetdisk\新素材\新素材\Obama\Obama_Openning.mp4'
    # BackendManagement.addVideoToCharacter(path, 'obama', 'opening')
