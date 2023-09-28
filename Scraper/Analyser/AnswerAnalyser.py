from bs4 import BeautifulSoup
import os

class AnswerAnalyser():
    @staticmethod
    def extractAndDiscover(dataStr:str)->dict:
        # extract
        bs = BeautifulSoup(dataStr, 'html.parser')
        questioncard = bs.select('.QuestionHeader-main')[0]

        questionTitle = questioncard.select('.QuestionHeader-title')[0]
        titleText = AnswerAnalyser.postProcess(questionTitle.getText())

        questionContent = questioncard.select('.QuestionRichText')[0]
        qContentText = AnswerAnalyser.postProcess(questionContent.getText())

        answercard = bs.select('.AnswerCard')
        textspan = answercard[0].select('.RichText')[0]
        answerText = AnswerAnalyser.postProcess(textspan.getText())

        # discover
        questionTopic = bs.select('.QuestionHeader-topics')[0]
        questionTopicsElem = questionTopic.select('.TopicLink > div')
        topics = [AnswerAnalyser.postProcess(topic.getText()) for topic in questionTopicsElem]

        return {
            'titleText': titleText,
            'qContentText': qContentText,
            'answerText': answerText,
            'topics': topics
        }
        pass

    @staticmethod
    def test():
        path = os.path.abspath('../')
        html = os.path.join(path, 'resource/answerHTML.html')
        with open(html,encoding='utf-8') as f:
            lines = f.readlines()
            htmlStr = ''.join(lines)
        result = AnswerAnalyser.extractAndDiscover(htmlStr)
        print(result)
        pass

    @staticmethod
    def postProcess(p):
        tokens = []
        while p.__contains__('<') or p.__contains__('>'):
            tks = p.split('<')
            tokens.append(tks[0])
            p = '<'.join(tks[1:])
            tks = p.split('>')
            p = '>'.join(tks[1:])
        tokens.append(p)

        return ''.join(tokens).replace('\n', '').replace('\t', '')
        pass
    pass

if __name__ == '__main__':
    AnswerAnalyser.test()