import os

from Config.Config import Config
from Config.VoiceModel import VoiceModel
from MovieMaker import TTS
from MovieMaker.Character import Character
from MovieMaker.Strategy import Strategy
from MovieMaker.TTSAgent import TTSAgent
from Scraper.Enums import Status
from Scraper.Enums.IdType import IdType
from Utils.DBUtils import DBUtils
from Utils.LLMUtils import LLMUtils
# from chatglm3.basic_demo.inference import ChatglmClient


class QuestionPicker:
    @staticmethod
    def process():
        pickedData = QuestionPicker.pickQuestion()
        print(f'picked data: {[p["questiontext"] for p in pickedData]}. {len(pickedData)} total')
        QuestionPicker.bookTask(pickedData)
        # ChatglmClient.clearDistance()
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
            question = Config.hostspeech.replace('{question}',
                                                 question)  # f'{question}, 我精心挑选了三个热心网友的回答，大家看看谁聊得更精彩，那么咱们现在开始吧！'

            # question
            questionPieces = TTSAgent.splitText(question)
            leader = Character.fromId(Strategy.getSpeechHostCharacterId())  # Character.randomCharacter()
            for i in range(0, len(questionPieces)):
                piece = questionPieces[i]
                ttsTask = TTSTaskEntry()
                ttsTask.qnaid = 0
                ttsTask.answerid = IdType.convertQuestion(questionid, -1, '', '')
                ttsTask.characterid = leader.id
                ttsTask.text = piece
                ttsTask.voice = leader.voice
                tasklist.append(ttsTask)

            characterIdLIst = Strategy.getSpeechActorIdList()
            answerTexts = []
            for i in range(0, len(top3answer)):
                entry = top3answer[i]
                qnaid = entry[0]
                answerid = entry[1]
                answer = entry[2]
                voteupcount = entry[3]

                answerTexts.append(answer)
                answerer = Character.fromId(characterIdLIst[i])
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
            conclusion = QuestionPicker.GenerateConclusion(question, answerTexts)  # Config.conclusionspeech

            ttsTask = TTSTaskEntry()
            ttsTask.qnaid = 0
            ttsTask.answerid = IdType.convertQuestion(questionid, -1, '', '')
            ttsTask.characterid = leader.id
            ttsTask.text = conclusion
            ttsTask.voice = leader.voice
            tasklist.append(ttsTask)
            db = DBUtils()
            db.newTask(questionid, [str(item[1]) for item in top3answer], tasklist)
            print(f'new task set. {len(tasklist)} total.')
            db.setQnaStatus([str(ele[0]) for ele in top3answer], Status.taskStatus.complete)
            db.close()
        pass

    @staticmethod
    def pickQuestion() -> list:
        recalldata = QuestionPicker.recall(Config.recalllimit)
        filtereddata = [item for item in recalldata if QuestionPicker.filter(item)]
        # 给已审过滤的结果打标
        QuestionPicker.ignoreSignToDroppedRecall(recalldata, filtereddata)
        answerfiltereddata = QuestionPicker.answerfiltereddata(filtereddata)
        rankedData = QuestionPicker.rank(answerfiltereddata)
        postprocessedData = QuestionPicker.postprocess(answerfiltereddata)
        return rankedData
        pass

    @staticmethod
    def rankanswer(answerlist):
        return answerlist

    @staticmethod
    def answerfiltereddata(data, take=3):
        for d in data:
            answerlist = QuestionPicker.rankanswer(d['answerlist'])
            d['answerlist'] = answerlist[0:take]
        return data

    @staticmethod
    def recall(limit: int, minlength: int = 50):
        db = DBUtils()
        # touchedQuestions = db.doQuery('select QuestionTitle from zhihu2bilibili.qna where taskgen != 0')
        result = db.doQuery(
            f'select QuestionTitle, Sum(VoteUpCount) as votesum, count(1) as cnt from '
            f'(SELECT idQnA, AnswerId, QuestionTitle, Answer, VoteUpCount, taskgenerated FROM zhihu2bilibili.qna'
            f' where length(answer) > 30'
            f' and length(answer) < 600'
            f' and VoteUpCount > 5'
            f' and TagMark="100010_2023-11-11"'
            f' and taskgenerated=0) availableData '
            f'group by QuestionTitle having cnt >= 3 order by votesum desc limit {limit}')
        resultlist = []
        print(f'question fetched: {[q[0] for q in result]}')
        for row in result:
            question = row[0]
            top3answer = db.doQuery(
                f'select idqna, answerid, Answer , voteupcount from zhihu2bilibili.qna where questiontitle = "{question}" and length(Answer) > {minlength} order by voteupcount desc limit 5')
            zhihuqid = IdType.stripId(top3answer[0][1]).split('_')[0]
            if len(top3answer) < 3:
                continue
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
        answerlist = data['answerlist']
        answerlongenough = [l for l in answerlist if Strategy.filterAnswer(l[2])]
        data['answerlist'] = answerlongenough
        return len(answerlongenough) >= 3
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

    @staticmethod
    def testLLMChat():
        while True:
            query = input("input:")
            if query.lower() == 'quit':
                break
            response = LLMUtils.askChatGLM3(query)
            print(f"chatglm:{response}")
        pass

    @staticmethod
    def testLLMConclusion():
        db = DBUtils()
        while True:
            query = input("input question id:")
            if query.lower() == 'quit':
                break
            question, answer1, answer2, answer3 = db.top3answersByQuestionId(query)
            if question is None:
                print("No such question.")
                continue
            response = LLMUtils.commentFor3qna(question, answer1, answer2, answer3)
            print("--------------------------------------")
            print(f"question:{question}")
            print(f"answer1:{answer1}")
            print(f"answer2:{answer2}")
            print(f"answer3:{answer3}")
            print(f"chatglm conclusion:{response}")
            print("--------------------------------------")

    @staticmethod
    def ignoreSignToDroppedRecall(recalldata, filtereddata):
        questionset = set([q['questiontext'] for q in recalldata])
        filteredQuestionSet = set([q['questiontext'] for q in filtereddata])
        db = DBUtils()
        for q in questionset:
            if not filteredQuestionSet.__contains__(q):
                db.updateQnaTaskStatusByQuestionText(q, Status.taskStatus.failed)
        db.close()
        pass

    # 后处理
    @staticmethod
    def postprocess(answerfiltereddata):
        for qnapair in answerfiltereddata:
            answerlist = qnapair['answerlist']
            for i in range(0, len(answerlist)):
                answer = answerlist[i]
                answerlist[i] = QuestionPicker.postprocessAnswer(answer)
        return answerfiltereddata
        pass

    @staticmethod
    def postprocessAnswer(answer):
        return answer
        pass

    @staticmethod
    def GenerateConclusion(question, answerTexts):
        return Config.conclusionspeech
        # responseText = LLMUtils.commentFor3qna(question, answerTexts[0], answerTexts[1], answerTexts[2])
        # return responseText
        pass


# zh-CN-XiaoyiNeural 女
# zh-CN-YunxiNeural 男
if __name__ == '__main__':
    QuestionPicker.testLLMConclusion()
