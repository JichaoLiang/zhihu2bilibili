import os

from MovieMaker import TTS
from Scraper.Enums.IdType import IdType
from Utils.DBUtils import DBUtils


class QuestionPicker:
    @staticmethod
    def process():
        pickedData = QuestionPicker.pickQuestion()
        QuestionPicker.bookTask(pickedData)
        pass

    @staticmethod
    def bookTask(pickedData):
        for questionEntity in pickedData:
            question = questionEntity['questionid']
            top3answer = questionEntity['answerlist']
        pass

    @staticmethod
    def pickQuestion()->list:
        recalldata = QuestionPicker.recall(20)
        filtereddata = [item for item in recalldata if QuestionPicker.filter(item)]
        rankedData = QuestionPicker.rank(filtereddata)
        return rankedData
        pass

    @staticmethod
    def recall(limit:int):
        db = DBUtils()
        result = db.doQuery(f'select QuestionTitle, Sum(VoteUpCount) as votesum, count(1) as cnt, sum(taskgenerated) as taskgen from '
                            f'(SELECT idQnA, AnswerId, QuestionTitle, Answer, VoteUpCount, taskgenerated FROM zhihu2bilibili.qna where length(answer) > 100 and VoteUpCount > 10) availableData '
                            f'group by QuestionTitle having cnt >= 3 and taskgen = 0 order by votesum desc limit {limit}')
        resultlist = []
        for row in result:
            question = row[0]
            top3answer = db.doQuery(f'select idqna, Answer , voteupcount from zhihu2bilibili.qna where questiontitle = "{question}" order by voteupcount desc limit 3')
            zhihuqid = IdType.stripId(top3answer[0][1]).split('_')[0]
            resultlist.append({
                'questionid': zhihuqid,
                'answerlist': list(top3answer)
            })

        db.close()
        return resultlist
        pass

    @staticmethod
    def filter(data)->list:
        return True
        pass

    @staticmethod
    def rank(datalist: list)->list:
        return datalist
        pass

    @staticmethod
    def test():
        picked = QuestionPicker.pickQuestion()
        print(picked)
        i = 0
        for row in picked:
            template = f'{row[1]}, 倾听下面的这个热心网友的回答： {row[2]}'
            toPath = os.path.abspath(f'../Resource/Product/dev/tts_{i}.wav')
            TTS.edgeTTS(template, 'zh-CN-YunxiNeural', toPath)
            i+=1

# zh-CN-XiaoyiNeural 女
# zh-CN-YunxiNeural 男
if __name__ == '__main__':
    QuestionPicker.test()