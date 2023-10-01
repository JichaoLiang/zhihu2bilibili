from bs4 import BeautifulSoup
import os
import munch
from Utils import CommonUtils as ut

class AnswerAnalyser():
    @staticmethod
    def buildRequestURL(id:str)->str:
        qna = id.split('_')
        return f'https://www.zhihu.com/question/{qna[0]}/answer/{qna[1]}'
        pass

    @staticmethod
    def extractAndDiscover(dataStr:str):
        # extract
        bs = BeautifulSoup(dataStr, 'html.parser')
        questioncard = bs.select('.QuestionHeader-main')[0]

        questionTitle = questioncard.select('.QuestionHeader-title')[0]
        titleText = ut.CommonUtils.htmlToText(questionTitle.getText())

        try:
            questionContent = questioncard.select('.QuestionRichText')[0]
            qContentText = ut.CommonUtils.htmlToText(questionContent.getText())
        except:
            qContentText = ''

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
            'topics': topics,
            'topicIdList': topicIdlist
        })
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