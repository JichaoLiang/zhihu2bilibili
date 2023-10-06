import time
import uuid

import pymysql


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
            cursor.execute(sql)
            result = cursor.fetchall()
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

    def newCharacter(self, name, gender, voice, picGroupList):
        if len(picGroupList) == 0:
            raise Exception('no pic to character is not allowed')
        groupid = picGroupList[0][0]
        commlist = [('insert into `zhihu2bilibili`.`picresourcedata` (PicGroupId, IndexInGroup, RelPath, Tag)'
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
        sql = (f'select picgroupid, relpath from zhihu2bilibili.picresourcedata where picgroupid="{groupid}" order by indexingroup asc')
        return self.doQuery(sql)

    @staticmethod
    def escapeSql(string: str) -> str:
        return string.replace('\n', '').replace('\r', '').replace('\'', '\'\'').replace('"', ' ')
        pass


if __name__ == '__main__':
    DBUtils.test()
