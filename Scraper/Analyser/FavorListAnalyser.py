

from bs4 import BeautifulSoup
import os
import json
import Utils
import munch
from Utils import CommonUtils as ut

# url sample
# https://www.zhihu.com/api/v4/answers/2708330353/favlists?include=data%5B*%5D.answer_count%2Cfollower_count%2Ccreator&offset=0&limit=10

class FavorListAnalyser():
    @staticmethod
    def buildRequestURL(id)->str:
        return f'https://www.zhihu.com/api/v4/answers/{id}/favlists?include=data%5B*%5D.answer_count%2Cfollower_count%2Ccreator&offset=0&limit=10'
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
        path = os.path.abspath('../')
        html = os.path.join(path, 'resource/favlist.json')
        with open(html,encoding='utf-8') as f:
            lines = f.readlines()
            htmlStr = ''.join(lines)
        result = FavorListAnalyser.extractAndDiscover(htmlStr)
        print(result)
        pass
    pass


if __name__ == '__main__':
    FavorListAnalyser.test()