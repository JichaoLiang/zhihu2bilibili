from bs4 import BeautifulSoup
import os
import json
import Utils
import munch
from Utils import CommonUtils as ut

# target url sample
# https://www.zhihu.com/api/v4/questions/323196827/similar-questions?include=data%5B*%5D.answer_count%2Cauthor%2Cfollower_count&limit=5&offset=0

class RelatedQuestionAnalyser():
    @staticmethod
    def buildRequestURL(id:str)->str:
        return f'https://www.zhihu.com/api/v4/questions/{id}/similar-questions?include=data%5B*%5D.answer_count%2Cauthor%2Cfollower_count&limit=10&offset=0'
        pass

    @staticmethod
    def extractAndDiscover(dataStr:str)->list:
        # extract
        jsonobj = json.loads(dataStr)
        # discover
        data = jsonobj['data']
        answerlist = [munch.DefaultMunch.fromDict(
            {
                'id': ut.CommonUtils.tryFetch(item, ['id']),
                'title': ut.CommonUtils.tryFetch(item, ['title']),
                'time': ut.CommonUtils.tryFetch(item, ['updated_time']),
                'answers': ut.CommonUtils.tryFetch(item, ['answer_count']),
                'comments': ut.CommonUtils.tryFetch(item, ['comment_count']),
                'followers':ut.CommonUtils.tryFetch(item, ['follower_count'])
            }) for item in data]
        return answerlist
        pass

    @staticmethod
    def test():
        path = os.path.abspath('../../')
        html = os.path.join(path, 'resource/relatedquestions.json')
        with open(html,encoding='utf-8') as f:
            lines = f.readlines()
            htmlStr = ''.join(lines)
        result = RelatedQuestionAnalyser.extractAndDiscover(htmlStr)
        print(result)
        pass

    pass


if __name__ == '__main__':
    RelatedQuestionAnalyser.test()