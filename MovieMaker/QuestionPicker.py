import os

from Config.VoiceModel import VoiceModel
from MovieMaker import TTS
from MovieMaker.Character import Character
from MovieMaker.TTSAgent import TTSAgent
from Scraper.Enums import Status
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
        class TTSTaskEntry:
            qnaid = 0
            answerid = ''
            characterid = ''
            voice = VoiceModel.default_male
            text = ''

        pass

        for questionEntity in pickedData:
            tasklist = []
            questionid = questionEntity['questionid']
            question = questionEntity['questiontext']
            top3answer = questionEntity['answerlist']

            # render question
            question = f'{question}, 我精心挑选了三个热心网友回答，大家看看谁聊得更精彩，那么咱们现在开始吧！'

            # question
            questionPieces = TTSAgent.splitText(question)
            leader = Character.randomCharacter()
            for i in range(0, len(questionPieces)):
                piece = questionPieces[i]
                ttsTask = TTSTaskEntry()
                ttsTask.qnaid = 0
                ttsTask.answerid = IdType.convertQuestion(questionid, -1, '', '')
                ttsTask.characterid = leader.id
                ttsTask.text = piece
                ttsTask.voice = leader.voice
                tasklist.append(ttsTask)

            for i in range(0, len(top3answer)):
                entry = top3answer[i]
                qnaid = entry[0]
                answerid = entry[1]
                answer = entry[2]
                voteupcount = entry[3]

                answerer = Character.randomCharacter()
                answerPieces = TTSAgent.splitText(answer)
                for j in range(0, len(answerPieces)):
                    piece = answerPieces[j]
                    ttsTask = TTSTaskEntry()
                    ttsTask.qnaid = qnaid
                    ttsTask.answerid = answerid
                    ttsTask.characterid = answerer.id
                    ttsTask.text = piece
                    ttsTask.voice = answerer.voice
                    tasklist.append(ttsTask)

            # conclusion
            conclusion = '听完了各位的回答，这次大家对他们的回答有什么想法呢？欢迎到评论区发出你的想法，咱们下期再见！'

            ttsTask = TTSTaskEntry()
            ttsTask.qnaid = 0
            ttsTask.answerid = IdType.convertQuestion(questionid, -1, '', '')
            ttsTask.characterid = leader.id
            ttsTask.text = conclusion
            ttsTask.voice = leader.voice
            tasklist.append(ttsTask)
            db = DBUtils()
            db.newTask(questionid, [str(item[1]) for item in top3answer], tasklist)
            db.setQnaStatus([ele[0] for ele in top3answer], Status.taskStatus.complete)
            db.close()
        pass

    @staticmethod
    def pickQuestion() -> list:
        recalldata = QuestionPicker.recall(20)
        filtereddata = [item for item in recalldata if QuestionPicker.filter(item)]
        rankedData = QuestionPicker.rank(filtereddata)
        return rankedData
        pass

    @staticmethod
    def recall(limit: int):
        db = DBUtils()
        result = db.doQuery(
            f'select QuestionTitle, Sum(VoteUpCount) as votesum, count(1) as cnt, sum(taskgenerated) as taskgen from '
            f'(SELECT idQnA, AnswerId, QuestionTitle, Answer, VoteUpCount, taskgenerated FROM zhihu2bilibili.qna where length(answer) > 100 and VoteUpCount > 10) availableData '
            f'group by QuestionTitle having cnt >= 3 and taskgen = 0 order by votesum desc limit {limit}')
        resultlist = []
        for row in result:
            question = row[0]
            top3answer = db.doQuery(
                f'select idqna, answerid, Answer , voteupcount from zhihu2bilibili.qna where questiontitle = "{question}" order by voteupcount desc limit 3')
            zhihuqid = IdType.stripId(top3answer[0][1]).split('_')[0]
            resultlist.append({
                'questionid': zhihuqid,
                'questiontext': question,
                'answerlist': list(top3answer)
            })

        db.close()
        return resultlist
        pass

    @staticmethod
    def filter(data) -> list:
        return True
        pass

    @staticmethod
    def rank(datalist: list) -> list:
        return datalist
        pass

    @staticmethod
    def test():
        QuestionPicker.process()
        # picked = QuestionPicker.pickQuestion()
        # print(picked)
        # i = 0
        # for row in picked:
        #     template = f'{row[1]}, 倾听下面的这个热心网友的回答： {row[2]}'
        #     toPath = os.path.abspath(f'../Resource/Product/dev/tts_{i}.wav')
        #     TTS.edgeTTS(template, 'zh-CN-YunxiNeural', toPath)
        #     i += 1


# zh-CN-XiaoyiNeural 女
# zh-CN-YunxiNeural 男
if __name__ == '__main__':
    QuestionPicker.test()
