from bs4 import BeautifulSoup
import os
import json
import Utils

# target url sample
# https://www.zhihu.com/api/v4/questions/323196827/similar-questions?include=data%5B*%5D.answer_count%2Cauthor%2Cfollower_count&limit=5
class RelatedQuestionAnalyser():
    @staticmethod
    def extractAndDiscover(dataStr:str)->dict:
        # extract
        jsonobj = json.loads(dataStr)
        # discover
        data = jsonobj['data']
        title = ''
        if len(data) > 0:
            question = Utils.CommonUtils.tryFetch(data[0],['target','question'])
            id = Utils.CommonUtils.tryFetch(question, ['id'])
        answerlist = [Utils.CommonUtils.tryFetch(item,['target','id']) for item in data]
        return {
            'questionId': id,
            'answeridlist': answerlist,
        }
        pass

    @staticmethod
    def test():
        path = os.path.abspath('../')
        html = os.path.join(path, 'resource/relatedquestions.json')
        with open(html,encoding='utf-8') as f:
            lines = f.readlines()
            htmlStr = ''.join(lines)
        result = RelatedQuestionAnalyser.extractAndDiscover(htmlStr)
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
    RelatedQuestionAnalyser.test()