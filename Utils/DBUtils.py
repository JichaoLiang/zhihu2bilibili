import time

import pymysql


class DBUtils:
    @staticmethod
    def test():
        db = DBUtils()
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

    @staticmethod
    def escapeSql(string:str)->str:
        return string.replace('\n','').replace('\r','').replace('\'','\'\'').replace('"', ' ')
        pass

if __name__ == '__main__':
    DBUtils.test()
