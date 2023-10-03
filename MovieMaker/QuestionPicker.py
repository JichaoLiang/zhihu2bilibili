import os

from MovieMaker import TTS
from Utils.DBUtils import DBUtils


class QuestionPicker:
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
        result = db.doQuery(f'select QuestionTitle,Answer from zhihu2bilibili.qna where `time` > "2023-10-3" and length(Answer) > 50 order by VoteUpCount desc limit {limit}')
        return list(result)
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
            template = f'{row[0]}, 倾听下面的这个热心网友的回答： {row[1]}'
            toPath = os.path.abspath(f'../Resource/Product/dev/tts_{i}.wav')
            TTS.edgeTTS(template, 'zh-CN-YunxiNeural', toPath)
            i+=1

# zh-CN-XiaoyiNeural 女
# zh-CN-YunxiNeural 男
if __name__ == '__main__':
    QuestionPicker.test()