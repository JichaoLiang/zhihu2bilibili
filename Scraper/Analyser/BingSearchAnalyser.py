import urllib
import urllib.parse
from bs4 import BeautifulSoup
import os
import munch

from Scraper.Enums.IdType import IdType
from Utils import CommonUtils as ut

# html
# https://www.zhihu.com/topic/19551275/hot
# feed
# https://www.zhihu.com/api/v5.1/topics/19551275/feeds/essence?offset=40&limit=20&
class BingSearchAnalyser():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": "__snaker__id=kz4NFu3D5cvOrK21; _zap=a76ce729-4a8d-49d8-b447-8161ebfb0956; "
                  "d_c0=AFATjOukcRePTmL_1bARTis9Bys9xPP9QB0=|1695543525; "
                  "YD00517437729195%3AWM_TID=Ap6FvWBKH3lABVEUBQaF3KA8ZWcXHhIi; "
                  "_xsrf=ac5a7a98-ddd2-4381-9eb0-172a12528115; "
                  "Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1695543525,1695982812; "
                  "Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1696046093; "
                  "captcha_session_v2=2|1:0|10:1696046095|18:captcha_session_v2|88"
                  ":RllNY3UxVHdIZDB4WkZ0QWw0YTlXaGlRV1lrUi9POFEvMXlDb1JKcEdkV1Q2NVhEOHhjT2xtTFJnR0o4dEhmRw"
                  "==|1e96bd9adfdc41ace448856a95c8f7433bc3b10e831f4ab2be66cb408125b544; "
                  "YD00517437729195%3AWM_NI=G3FII7ntiLenx3tukd489q8oYi%2FzGhGvJNFHTOPVeRQo7Q1RaV6eS3w7Cv"
                  "%2FIu9NqKi8PnDke8iyiIbfijY0zy7zawqVTaFcvg1HdN9lAPWSIryFPa2H5Hzmlz%2F5qeERJMXk%3D; "
                  "YD00517437729195%3AWM_NIKE"
                  "=9ca17ae2e6ffcda170e2e6eea6ef4391ae8bb6e273b1ac8ba2c54a869e8ab0d43a90b698b6cc54b7aa9c92b82af0fea7c3b92a85ed8aaacc3daeaca7ade866bcedbc96ea70f8e8f792bb659bb7e19bc66485aa86afc5449891a0b7e85a93b1f9b2b45aa38afa86d239b5e98d97ae43b7e78292ca63fc90a2a5ea6ffcb7b78acc6aa6b7a6bab372bbe9b682f67b968cafa7e27ea5ef8885cd33b09fa0b8d243b2a78ab1e43a8ceb889bf068baf1fb92e84f929683b9ea37e2a3; gdxidpyhxdE=Vf6kflyVyHxDCM2HZ8ecws%2Bx2j9R4Dhbstofr%2Fr6E0C79xSJx%2FGeCDWNAp7sAOyijlH%5CcNtbX%2Fga5GRrdXoazMeqZP1kVGu1bUMIjoneiZGoCO%5CPTMGckuC141UV2iZtx%2FJNo6K%5C4P3OOgpU07o3wq1JcfvAoRCBi6aBTxv1fVLMiLHH%3A1696147794305; KLBRSID=76ae5fb4fba0f519d97e594f1cef9fab|1696146949|1696146881"
    }
    @staticmethod
    def buildRequestURL(id:str)->str:
        keyword = id
        query = keyword + " 知乎"
        urlTemplate = f"https://cn.bing.com/search?{urllib.parse.urlencode({'q': query})}"
        return urlTemplate
        pass
    @staticmethod
    def zhihuPickedRulePassed(siteUrl):
        if siteUrl.startswith('https://www.zhihu.com') and siteUrl.__contains__('question'):
            return True
        return False
        pass

    @staticmethod
    def extractAndDiscover(dataStr:str):
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
                    if BingSearchAnalyser.zhihuPickedRulePassed(siteUrl):
                        # https://www.zhihu.com/question/456284918/answer/3221454349
                        question = siteUrl.split('question/')[-1].split('/')[0]
                        # answer = siteUrl.split('answer/')[-1]
                        qnalist.append(question)
            except Exception as ex:
                print(str(ex))
                continue

        return munch.DefaultMunch.fromDict({
            'qnaPairList': qnalist
        })
        pass
    #
    # @staticmethod
    # def zhihuPickedRulePassed(siteUrl):
    #     # if siteUrl.startswith('https://zhidao.baidu.com'):
    #     #     return True
    #     # if siteUrl.startswith('https://baike.baidu.com'):
    #     #     return True
    #     if siteUrl.startswith('https://www.zhihu.com'):
    #         return True
    #     return False
    #     pass
    @staticmethod
    def test():
        path = os.path.abspath('../../')
        html = os.path.join(path, 'resource/topic.html')
        with open(html,encoding='utf-8') as f:
            lines = f.readlines()
            htmlStr = ''.join(lines)
        result = BingSearchAnalyser.extractAndDiscover(htmlStr)
        print(result)
        pass

    pass

if __name__ == '__main__':
    BingSearchAnalyser.test()