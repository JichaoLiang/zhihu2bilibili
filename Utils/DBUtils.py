import os.path
import time
import uuid

import pymysql

from Scraper.Enums import Status


class DBUtils:
    @staticmethod
    def test():
        db = DBUtils()
        print(db.taskRemaining())
        return
        db.answerExists('123123')
        title = 'hello'
        content = 'thank you'
        answer = 'thank you very much'
        tagMark = 'test'
        topics = ['aaa', '矮点辅料']
        topicIds = ['123123', '12342134']
        updated = 123123
        voteCount = 123
        commentCount = 456
        isCollapsed = 0
        db.newAnswer(
            '111',
            title,
            content,
            answer,
            updated,
            topics,
            topicIds,
            voteCount,
            commentCount,
            tagMark,
            isCollapsed
        )
        pass

    def __init__(self):
        pass

    connection = None

    def tryConnect(self):
        if self.connection is None:
            self.connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='tk1372353',
                db='zhihu2bilibili',
                charset='utf8',
            )
        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection.close()
        return

    # result format tuple ((1,2,3...),()...)
    def doQuery(self, sql):
        connect = self.tryConnect()
        with connect.cursor() as cursor:
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
            except Exception as ex:
                print(f'debug sql: {sql}')
                raise ex
        return result

    def doCommand(self, sql):
        connect = self.tryConnect()
        with connect.cursor() as cursor:
            cursor.execute(sql)
        connect.commit()

    def doCommands(self, sqllist):
        connect = self.tryConnect()
        for sql in sqllist:
            with connect.cursor() as cursor:
                cursor.execute(sql)
        connect.commit()

    def answerExists(self, answerId):
        result = self.doQuery(
            f'select count(1) from `zhihu2bilibili`.`qna` where AnswerId="{answerId}"'
        )
        return result[0][0] > 0

    def newAnswer(self, answerId, questionTitle, questionContent, answerText, updated, topics, topicIds, voteUpCount,
                  commentCount, tagmark, isCollapsed):
        localtime = time.localtime(updated)
        timestr = time.strftime('%Y-%m-%d %H:%M:%S', localtime)
        comm = ('INSERT INTO `zhihu2bilibili`.`qna`'
                ' ('
                '`AnswerId`,'
                '`QuestionTitle`,'
                '`QuestionContent`,'
                '`Answer`,'
                '`TagMark`,'
                '`VoteUpCount`,'
                '`CommentCount`,'
                '`Time`,'
                '`Updated`,'
                '`Topics`,'
                '`TopicId`,'
                '`isCollapsed`)'
                'VALUES'
                '('
                f'"{answerId}",'
                f'"{DBUtils.escapeSql(questionTitle)}",'
                f'"{DBUtils.escapeSql(questionContent)}",'
                f'"{DBUtils.escapeSql(answerText)}",'
                f'"{tagmark}",'
                f'{voteUpCount},'
                f'{commentCount},'
                'NOW(),'
                f'"{timestr}",'
                f'"{topics}",'
                f'"{topicIds}",'
                f'{isCollapsed});')
        self.doCommand(comm)

    pass

    def newCharacter(self, name, gender, voice, picGroupList, videoGroupList):
        if len(picGroupList) == 0 and len(videoGroupList) == 0:
            raise Exception('no pic and no video to character is not allowed')

        groupid = None
        videogroupid = None
        commlist = []
        if len(picGroupList) > 0:
            groupid = picGroupList[0][0]
            commlist += [('insert into `zhihu2bilibili`.`picresourcedata` (PicGroupId, IndexInGroup, RelPath, Tag)'
                          f' values ("{pic[0]}", {pic[1]},"{pic[2]}","{pic[3]}");')
                         for pic in picGroupList]
        if len(videoGroupList) > 0:
            videogroupid = videoGroupList[0][0]
            commlist += [('insert into `zhihu2bilibili`.`videoresourcedata` (VideoGroupId, IndexInGroup, RelPath, Tag)'
                          f' values ("{video[0]}", {video[1]},"{video[2]}","{video[3]}");')
                         for video in videoGroupList]
        if groupid != None and videogroupid != None:
            targetFieldName = 'picgroupid, videogroupid'
            targetVal = f'"{groupid}", "{videogroupid}"'
        elif groupid != None:
            targetFieldName = 'picgroupid'
            targetVal = f'"{groupid}"'
        elif videogroupid != None:
            targetFieldName = 'videogroupid'
            targetVal = f'"{videogroupid}"'
        commlist.append((f'insert into `zhihu2bilibili`.`character` (name, gender, voice, {targetFieldName}) '
                         f'values ("{name}", {gender}, "{voice}", {targetVal});'))
        self.doCommands(commlist)
        pass

    def newVideoCharacter(self, name, gender, voice, picGroupList):
        if len(picGroupList) == 0:
            raise Exception('no video to character is not allowed')
        groupid = picGroupList[0][0]
        commlist = [('insert into `zhihu2bilibili`.`videoresourcedata` (VideoGroupId, IndexInGroup, RelPath, Tag)'
                     f' values ("{pic[0]}", {pic[1]},"{pic[2]}","{pic[3]}");')
                    for pic in picGroupList]
        commlist.append((f'insert into `zhihu2bilibili`.`character` (name, gender, voice, picgroupid) '
                         f'values ("{name}", {gender}, "{voice}", "{groupid}");'))
        self.doCommands(commlist)
        pass

    def taskRemaining(self):
        sql = ("select count(1) from zhihu2bilibili.taskstatus where TTSSuccess = 0"
               " or CharacterSuccess = 0"
               " or MovieSuccess = 0")
        result = self.doQuery(sql)
        return result[0][0]
        pass

    def newTask(self, questionid, answeridlist, tasklist):
        sql = (f'insert into zhihu2bilibili.taskstatus '
               f'(questionid, answerid) '
               f'values ("{questionid}","{",".join(answeridlist)}")')
        self.doCommand(sql)
        id = self.doQuery(f'select idTaskStatus from zhihu2bilibili.taskstatus where questionid="{questionid}"'
                          f' and answerid = "{",".join(answeridlist)}" order by idTaskStatus desc limit 1')[0][0]
        self.newTTSTask(id, tasklist)

    def newTTSTask(self, taskid, tasklist):
        sqllist = []
        for i in range(0, len(tasklist)):
            task = tasklist[i]
            sql = (f'INSERT INTO `zhihu2bilibili`.`ttstask`'
                   f'(`taskId`,`qnaid`,`characterid`,`voice`,`textchunk`,`textindex`)'
                   f'VALUES({taskid},{task.qnaid},{task.characterid},"{task.voice}","{task.text}",{i});')
            sqllist.append(sql)
        self.doCommands(sqllist)

    def characterById(self, id):
        sql = (f'SELECT * FROM zhihu2bilibili.character where idcharacter={id}')
        return self.doQuery(sql)[0]

    def randomCharacter(self):
        sql = (f'SELECT * FROM zhihu2bilibili.character order by rand() limit 1;')
        return self.doQuery(sql)[0]

    def randomMale(self):
        sql = (f'SELECT * FROM zhihu2bilibili.character where gender=1 order by rand() limit 1;')
        return self.doQuery(sql)[0]

    def randomFemale(self):
        sql = (f'SELECT * FROM zhihu2bilibili.character where gender=0 order by rand() limit 1;')
        return self.doQuery(sql)[0]

    def getPicListByCharacterId(self, id):
        sql = (f'select picgroupid from zhihu2bilibili.character where idcharacter={id}')
        groupid = self.doQuery(sql)[0][0]
        sql = (
            f'select picgroupid, relpath, tag from zhihu2bilibili.picresourcedata where picgroupid="{groupid}" order by indexingroup asc')
        return self.doQuery(sql)

    def getVideoListByCharacterId(self, id):
        sql = (f'select videogroupid from zhihu2bilibili.character where idcharacter={id}')
        groupid = self.doQuery(sql)[0][0]
        sql = (
            f'select videogroupid, relpath, tag from zhihu2bilibili.videoresourcedata where videogroupid="{groupid}" order by indexingroup asc')
        return self.doQuery(sql)
        pass

    def setQnaStatus(self, qnaID, status: int):
        sql = (f'update zhihu2bilibili.qna '
               f'set `taskGenerated`={status} '
               f'where `idQnA` in ({",".join([str(q) for q in qnaID])})')
        self.doCommand(sql)
        pass

    def setTaskStatus(self, taskId: str, ttsStatus: int, aiGeneratedStatus: int, movieGenerated: int):
        if ttsStatus < 0 and aiGeneratedStatus < 0 and movieGenerated < 0:
            return
        setfield = []
        if ttsStatus > 0:
            setfield.append(f'`ttssuccess`={ttsStatus}')
        if aiGeneratedStatus > 0:
            setfield.append(f'`charactersuccess`={aiGeneratedStatus}')
        if movieGenerated > 0:
            setfield.append(f'`moviesuccess`={movieGenerated}')

        sql = (f'update zhihu2bilibili.taskstatus '
               f'set '
               f'{",".join(setfield)} '
               f'where idTaskStatus={taskId}')
        self.doCommand(sql)
        pass

    def fetchTTSJob(self):
        sql = (f'select * from zhihu2bilibili.ttstask'
               f' where wavpath=""')
        return self.doQuery(sql)

    def fetchVideoChunk(self, taskstatusidlist):
        sql = (f'select * from zhihu2bilibili.videochunk'
               f' where taskstatusid in ({",".join([str(ids) for ids in taskstatusidlist])})')
        return self.doQuery(sql)

    def fetchVideoChunkList(self, taskstatusid):
        sql = (f'select * from zhihu2bilibili.videochunk'
               f' where taskstatusid = {taskstatusid} order by `index` asc')
        return self.doQuery(sql)

    def fetchVideoGenerationJob(self):
        sql = (f'select idTaskStatus from zhihu2bilibili.taskstatus'
               f' where TTSSuccess="{Status.taskStatus.complete}" and CharacterSuccess="{Status.taskStatus.waiting}"')
        return self.doQuery(sql)
        pass

    def fetchMovieMakerJob(self):
        sql = (f'select idTaskStatus from zhihu2bilibili.taskstatus'
               f' where CharacterSuccess="{Status.taskStatus.complete}" and MovieSuccess="{Status.taskStatus.waiting}"')
        return self.doQuery(sql)
        pass

    def fetchVideoGenerationVoiceList(self, taskid):
        sql = (f'select * from zhihu2bilibili.ttstask'
               f' where taskid={taskid} order by textindex asc')
        return self.doQuery(sql)
        pass

    def updateVoicePath(self, id, wavId):
        sql = (f'update zhihu2bilibili.ttstask '
               f'set wavpath="{wavId}" where idttstask={id}')
        self.doCommand(sql)
        pass

    def newVideoChunkPath(self, task, charater, index, fileid):
        sql = (f'insert into zhihu2bilibili.videochunk'
               f'(taskStatusId,videochunkpath, characterid, `index`) '
               f'values({task},"{fileid}",{charater},{index})')
        self.doCommand(sql)
        pass

    def bookVideoChunkJob(self, id):
        sql = (f'insert into zhihu2bilibili.videochunk'
               f'(ttstaskid) '
               f'values({id})')
        self.doCommand(sql)
        pass

    @staticmethod
    def escapeSql(string: str) -> str:
        return string.replace('\n', '').replace('\r', '').replace('\'', '\'\'').replace('"', ' ')
        pass

    def getAnswersByTaskstatusId(self, taskid):
        sql = f'select answerid from zhihu2bilibili.taskstatus where idtaskstatus = {taskid}'
        result = self.doQuery(sql)
        return result
        pass

    def getQnaByAnswerId(self, answerid):
        sql = f'select * from zhihu2bilibili.qna where answerid ="{answerid}"'
        return self.doQuery(sql)
        pass

    def newAudio(self, name, groupid, index, pathid, tag):
        sql = (f'insert into zhihu2bilibili.audioresourcedata(audiogroupid,name,indexingroup,relpath,tag)'
               f' values("{groupid}","{name}",{index}, "{pathid}", "{tag}")')
        self.doCommand(sql)
        pass

    def getVoiceByTag(self, tag):
        sql = f'select * from zhihu2bilibili.audioresourcedata where tag="{tag}"'
        return self.doQuery(sql)
        pass

    def getVideoListByTag(self, tag):
        sql = f'select * from zhihu2bilibili.videoresourcedata where tag="{tag}"'
        return self.doQuery(sql)
        pass

    def updateQnaTaskStatusByQuestionText(self, question, status):
        sql = f'update zhihu2bilibili.qna set taskGenerated={status} where QuestionTitle="{question}"'
        self.doCommand(sql)
        pass


if __name__ == '__main__':
    DBUtils.test()
