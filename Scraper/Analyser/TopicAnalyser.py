from bs4 import BeautifulSoup
import os
import munch
from Utils import CommonUtils as ut

# html
# https://www.zhihu.com/topic/19551275/hot
# feed
# https://www.zhihu.com/api/v5.1/topics/19551275/feeds/essence?offset=40&limit=20&
class TopicAnalyser():
    @staticmethod
    def buildRequestURL(id:str)->str:
        return f'https://www.zhihu.com/topic/{id}/hot'
        pass

    @staticmethod
    def extractAndDiscover(dataStr:str):
        # extract
        bs = BeautifulSoup(dataStr, 'html.parser')
        titleDiv = bs.select('.TopicMetaCard')
        title = ut.CommonUtils.tryFetchHtml(bs,['.TopicMetaCard', '.TopicMetaCard-title'])
        if len(title) > 0:
            titleText = ut.CommonUtils.htmlToText(title[0].get_text())

        questioncard = bs.select('.TopicFeedItem')

        # discover
        questionIdList = []
        for card in questioncard:
            link = ut.CommonUtils.tryFetchHtml(card,['a'])[0]
            url = link['href']
            if ut.UrlType.getUrlType(url) == ut.UrlType.answer:
                questionIdList.append(url.split('/')[-1])

        return munch.DefaultMunch.fromDict({
            'titleText': titleText,
            'questionIdList': questionIdList
        })
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