import urllib
import urllib.parse
from bs4 import BeautifulSoup
import os
import munch

from Scraper.Enums.IdType import IdType
from Utils import CommonUtils as ut


# 爬bing 记得关代理!!!
class BingSearchAnalyser():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "MUID=3B94E3408A8C6F0A0A4CF1348B976E27; _EDGE_V=1; SRCHD=AF=NOFORM; "
                  "SRCHUID=V=2&GUID=F8268E82B39849A7931EC5F7F56E05DF&dmnchg=1; "
                  "MUIDB=3B94E3408A8C6F0A0A4CF1348B976E27; "
                  "MicrosoftApplicationsTelemetryDeviceId=4683975d-c6fe-44a0-bd1b-ae5bf48f7873; PPLState=1; "
                  "SnrOvr=X=rebateson; MMCASM=ID=E0F9DB97F5744A70AD7270B1E638C941; "
                  "ANON=A=32A5624CED8D971858B5FD7FFFFFFFFF&E=1c80&W=1; _UR=QS=0&TQS=0&cdxcls=0; "
                  "NAP=V=1.9&E=1c8e&C=gzwiKvBOEPeOW4Wj4266WaIcHTLVA3cDmtiD-7hcaRKgKLJCblCtFA&W=1; "
                  "KievRPSSecAuth=FAByBBRaTOJILtFsMkpLVWSG6AN6C"
                  "/svRwNmAAAEgAAACPVUHhwLDv4HMAQ6ScRGqdTLSzIRdxQHogDlx1dTjnOqKXK5OBNTp14TSCHGO5xM5AsMvx"
                  "+fcCswPI99vKa0Uc56/07Wvh5Ucy7qbegOUNCJIrZTCAOd0DqhNUsIe5powF88MEJyO3oefvPEWyYXVVSf2S2CIz2TWWF8b9"
                  "+suvmwBjWPs0HJS9bdVAS98liIes0iH++D"
                  "+LlUxkvGmIpr0oJQRUDiFmmZArC4Q3nkVzRawkfZna8jJupYkF2rweEAns1UUSQO2aUFDbPSvFGBRf"
                  "/g1w26J960QC2rN5tljOnI2sMKbpyJWxxLPFCTAm2GqW1D7cXfUFxdfMt2Z1e6IF7mqBACvQLvvuuOr0zgEVB72tmSM5zddRichwIxf7EeoXHxZ2ZhEQSC9PHeecY32fLCOmLBgr0MyKlkDUzUJku6WqzxktZenqxKUz5sRDl7gkmi/TL8utIReIix+vCseXS/V0MSjdO8X2XwaryreLmibYGkyqqGJti8eKgYHiUZ3iyKsdsYvVm56nWuftsalrMYyfZtUNxiBBgDkUyP0OS//LJKWQzK4YqaBseGABHWVdfzS13WFfyyuCcYlUpYvJnbJlaYRUG9TU+mWlEsPuZoZhsmis6gEM17qUH7DonPW0psAyG0+GJa8jurNpSZ6MiDDY02kARMM9lmJRc7kHKlJmLECeNkD8oTn9QL+fzMEdU9Wk2djfpaj0XROJtJzAzH7cUq/v0nacZYbN2sx4YqXQKrMfNJCbdydC67R37t5Cgg0luiF99eCileIFuV1ZWHv2T0LRz0HJNfDhC9mXg4qptxbUjimAUr76KnmB3OJTAZgtHhUrBfpiJZpsz6z4OuefsKpkZyHrdbGrtr98CQFfKYX/60sv0vrZyfD/qM0lps2maWTaPVsbBWFnDqBmThrNjKEZQfl84fwv+wjvv9jIvNHs+e1t7Qeh0PBNvJOFLF64zqf5T1F2xDstUVYawkwTvhLb506Dt/GDYPnz0rdQV5JE3ZJ+L1i+1+3Uni/3KE3JS4puiRpBJh462WR/ewpQ780h5hQeBdeDtQW4UXUzsn1kAp33ogACc/ghI6316djISoHkxTOyTJ/lDBz6bzfrSGVIOf6eMexq9Qh0a2/R5b0cOQ3Zr/3LmksJlMN8ii88yIDckB5l2JPAexeLNbIf96WQoXFKumoxotzWiiQ8ADPWip8Rfvaq3asI6/LYSaktIdIQqkZhXcBcDt+MLtKbKV+t933FJWg1dA+rLlUVCrlf7FuUbI/WkJU2IUwVMwq0NBZ8mSZXDXWCY24rr8nHmxdO3A6v7ZiQebPS96BDXLxTIEDT0Q9G16S7Bo5shPMbozIC0ZA31jxuAF0zwv2Uzf7jMpP+3xXQhZGPzMPMtJbb84Nm8K6+1123wl2pLMvLdNavRITMAkCp4zpMpu7j5dqm3BeG6YFACs/2/Y3g0KzJWbhALv+PBn55aVKw==; MSCCSC=1; _HPVN=CS=eyJQbiI6eyJDbiI6MTcsIlN0IjowLCJRcyI6MCwiUHJvZCI6IlAifSwiU2MiOnsiQ24iOjE3LCJTdCI6MCwiUXMiOjAsIlByb2QiOiJIIn0sIlF6Ijp7IkNuIjoxNywiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0xMS0yMVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjo2MSwiVG9iYnMiOjB9; ipv6=hit=1700571129835&t=4; _Rwho=u=d; ai_session=KzAUSY73GtHk7bq4dzJFmZ|1700567531095|1700567531095; USRLOC=HS=1&ELOC=LAT=39.96904373168945|LON=116.48928833007812|N=%E6%9C%9D%E9%98%B3%E5%8C%BA%EF%BC%8C%E5%8C%97%E4%BA%AC%E5%B8%82|ELT=6|; SRCHUSR=DOB=20221208&T=1700567529000&TPC=1700567542000; _SS=SID=28E3F85EECAF69DA09E6EB8EEDE5684E&R=441&RB=441&GB=0&RG=0&RP=441; _RwBf=ilt=23&ihpd=1&ispd=0&rc=441&rb=441&gb=0&rg=0&pc=441&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=5&l=2023-11-21T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=BINGCOPILOTWAITLIST&c=MR000T&t=3146&s=2023-05-13T06:41:56.6719363+00:00&ts=2023-11-21T11:55:36.9008507+00:00&rwred=0&wls=2&lka=0&lkt=0&TH=&r=1&mta=0&e=CDH4m6z6z-vKniIU_F76f-3kF9tgmYpNo3650x5qDBhq-_K1Glz1SyAhJRdnT8bq6I-T99K4O3wkpz_Yw59kdl5TAMFxIMiH90YY18IfjE8&A=&dci=0&wlb=0&aad=0; SRCHHPGUSR=SRCHLANG=zh-Hans&BRW=XW&BRH=T&CW=2560&CH=1291&SCW=2543&SCH=3274&DPR=1.0&UTC=480&DM=0&WTS=63836164329&HV=1700567737&PRVCW=662&PRVCH=1291&PV=10.0.0&BZA=0&IG=4C4C58128620429A8BE425BB2EA2C81D&EXLTT=2&CIBV=1.1342.2; _EDGE_S=SID=28E3F85EECAF69DA09E6EB8EEDE5684E&mkt=zh-cn "
    }

    @staticmethod
    def buildRequestURL(id: str) -> str:
        keyword = id
        query = keyword + " 知乎"
        urlTemplate = f"https://cn.bing.com/search?{urllib.parse.urlencode({'q': query})}"
        return urlTemplate, BingSearchAnalyser.header
        pass

    @staticmethod
    def zhihuPickedRulePassed(siteUrl):
        if siteUrl.startswith('https://www.zhihu.com') and siteUrl.__contains__('question'):
            return True
        return False
        pass

    @staticmethod
    def extractAndDiscover(dataStr: str):
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
        with open(html, encoding='utf-8') as f:
            lines = f.readlines()
            htmlStr = ''.join(lines)
        result = BingSearchAnalyser.extractAndDiscover(htmlStr)
        print(result)
        pass

    pass


if __name__ == '__main__':
    BingSearchAnalyser.test()
