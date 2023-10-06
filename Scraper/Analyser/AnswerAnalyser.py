import json

from bs4 import BeautifulSoup
import os
import munch
from Utils import CommonUtils as ut
from Utils.CommonUtils import CommonUtils


class AnswerAnalyser():
    @staticmethod
    def buildRequestURL(id:str)->str:
        qna = id.split('_')
        return f'https://www.zhihu.com/question/{qna[0]}/answer/{qna[1]}'
        pass

    @staticmethod
    def extractAndDiscover(dataStr:str, taskId: str):
        # extract
        bs = BeautifulSoup(dataStr, 'html.parser')
        questioncard = bs.select('.QuestionHeader-main')[0]

        questionTitle = questioncard.select('.QuestionHeader-title')[0]
        titleText = ut.CommonUtils.htmlToText(questionTitle.getText())

        try:
            # questionContent = questioncard.select('.QuestionRichText')[0]
            # qContentText = ut.CommonUtils.htmlToText(questionContent.getText())

            dataInitScript = bs.select('#js-initialData')
            if len(dataInitScript) > 0:
                dataJsonText = dataInitScript[0].get_text()
                jsonObj = json.loads(dataJsonText)
                questionNode = CommonUtils.tryFetch(jsonObj, ['initialState','entities','questions'])
                detail = questionNode[list(questionNode.keys())[0]]['detail']
                # decoded = bytes(detail, 'utf-8').decode('unicode_escape')
                qContentText = CommonUtils.htmlToText(detail)

                answerNode = CommonUtils.tryFetch(jsonObj, ['initialState','entities','answers'])
                defaultAnswer = answerNode[list(answerNode.keys())[0]]
                voteCount = defaultAnswer['voteupCount']
                commentCount = defaultAnswer['commentCount']
                collapsed = defaultAnswer['isCollapsed']
                updatedTime = defaultAnswer['updatedTime']
        except Exception as e:
            print('parse error: ' + str(e))
            qContentText = ''
            voteCount = 0
            commentCount = 0
            collapsed = False
            updatedTime = 0

        answercard = bs.select('.AnswerCard')
        textspan = answercard[0].select('.RichText')[0]
        answerText = ut.CommonUtils.htmlToText(textspan.getText())

        # discover
        questionTopic = bs.select('.QuestionHeader-topics')[0]
        questionTopicsElem = questionTopic.select('.TopicLink > div')
        topicIdlist = [div['href'].split('/')[-1] for div in questionTopic.select('.TopicLink')]
        topics = [ut.CommonUtils.htmlToText(topic.getText()) for topic in questionTopicsElem]

        return munch.DefaultMunch.fromDict({
            'titleText': titleText,
            'qContentText': qContentText,
            'answerText': answerText,
            'voteCount': voteCount,
            'commentCount': commentCount,
            'isCollapsed': collapsed,
            'topics': topics,
            'topicIdList': topicIdlist,
            'updated': updatedTime
        })
        pass

    @staticmethod
    def dataPickStrategy(entity):
        if len(entity.answerText) >= 1000:
            return f'answer to long: {len(entity.answerText)}'
        if len(str(entity.topicIdList)) >= 300:
            return f'topicId to long: {len(str(entity.topicIdList))}'
        if len(str(entity.topics)) >= 300:
            return f'topics to long: {len(str(entity.topics))}'
        if len(str(entity.titleText)) >= 200:
            return f'titleText to long: {len(str(entity.titleText))}'
        if len(str(entity.qContentText)) >= 500:
            return f'qContentText to long: {len(str(entity.qContentText))}'
        return 'ok'
        pass

    @staticmethod
    def test():
        path = os.path.abspath('../../')
        html = os.path.join(path, 'resource/answerHTML.html')
        with open(html,encoding='utf-8') as f:
            lines = f.readlines()
            htmlStr = ''.join(lines)
        result = AnswerAnalyser.extractAndDiscover(htmlStr)
        print(result)
        pass

    pass

if __name__ == '__main__':
    AnswerAnalyser.test()