import urllib

from bs4 import BeautifulSoup
import os
import munch

from Scraper.Enums.IdType import IdType
from Utils import CommonUtils as ut

# html
# https://www.zhihu.com/topic/19551275/hot
# feed
# https://www.zhihu.com/api/v5.1/topics/19551275/feeds/essence?offset=40&limit=20&
class BaiduSearchAnalyser():
    @staticmethod
    def buildRequestURL(id:str)->str:
        keyword = IdType.stripId(id)
        query = keyword + " 知乎"
        urlTemplate = f"https://cn.bing.com/search?{urllib.urlencode({'q': query})}"
        return urlTemplate
        pass
    @staticmethod
    def zhihuPickedRulePassed(siteUrl):
        if siteUrl.startswith('https://www.zhihu.com'):
            return True
        pass

    @staticmethod
    def extractAndDiscover(dataStr:str, id:str):
        textStr = dataStr
        qnalist = []
        bs = BeautifulSoup(textStr, 'html.parser')
        ol = bs.select('#b_results')[0]
        lis = ol.select('.b_algo')
        for li in lis:
            try:
                st = li.select('cite')
                if len(st) > 0:
                    site = st[0]
                    siteUrl = site.text
                    if BaiduSearchAnalyser.zhihuPickedRulePassed(siteUrl):
                        # https://www.zhihu.com/question/456284918/answer/3221454349
                        question = siteUrl.split('question/')[-1].split('/answer')[0]
                        answer = siteUrl.split('answer/')[-1]
                        qnalist.append([question, answer])
            except Exception as ex:
                print(str(ex))
                continue

        return munch.DefaultMunch.fromDict({
            'titleText': titleText,
            'questionIdList': questionIdList
        })
        pass

    @staticmethod
    def zhihuPickedRulePassed(siteUrl):
        if siteUrl.startswith('https://zhidao.baidu.com'):
            return True
        if siteUrl.startswith('https://baike.baidu.com'):
            return True
        if siteUrl.startswith('https://www.zhihu.com'):
            return True
        pass
    @staticmethod
    def test():
        path = os.path.abspath('../../')
        html = os.path.join(path, 'resource/topic.html')
        with open(html,encoding='utf-8') as f:
            lines = f.readlines()
            htmlStr = ''.join(lines)
        result = TopicAnalyser.extractAndDiscover(htmlStr)
        print(result)
        pass

    pass

if __name__ == '__main__':
    TopicAnalyser.test()