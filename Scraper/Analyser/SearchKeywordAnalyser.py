import os

import munch

from Scraper.Enums.IdType import IdType
from urllib.parse import urlencode
import json

from Utils.CommonUtils import CommonUtils


class SearchKeywordAnalyser:
    @staticmethod
    def buildRequestURL(rawid, header:dict=None)->str:
        encodedkeyword = CommonUtils.urlencodestring(rawid)
        if header is not None:
            header.setdefault('Referer', f'https://www.zhihu.com/search?type=content&q={encodedkeyword}')
        url = (f'https://www.zhihu.com/api/v4/search_v3?gk_version=gz-gaokao&t=general'
               f'&q={encodedkeyword}&correction=1&offset=0&limit=20&filter_fields=&lc_idx=40'
               f'&show_all_topics=0&search_hash_id=92ad710f74a712c67f7817e4d7156f45&search_source=Normal'
               f'&vertical_info=0%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C3')
        return url, header
        pass

    @staticmethod
    def extractAndDiscover(dataStr: str, taskId: str):
        jsonObj = json.loads(dataStr)
        datanode = CommonUtils.tryFetch(jsonObj, ['data'])
        idlist = [[CommonUtils.tryFetch(node,['object', 'id']),
                   CommonUtils.tryFetch(node, ['object', 'question', 'id'])]
                  for node in datanode
                  if CommonUtils.tryFetch(node,['object', 'type']) == 'answer']
        return munch.DefaultMunch.fromDict({
            'idlist': idlist
        })
        pass
    @staticmethod
    def test():
        path = os.path.abspath('../../')
        html = os.path.join(path, 'resource/searchresult.json')
        with open(html,encoding='utf-8') as f:
            lines = f.readlines()
            htmlStr = ''.join(lines)
        result = SearchKeywordAnalyser.extractAndDiscover(htmlStr, '')
        print(result)
        pass

    pass

if __name__ == '__main__':
    SearchKeywordAnalyser.test()