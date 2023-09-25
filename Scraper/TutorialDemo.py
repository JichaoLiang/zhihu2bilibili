import time

import requests
from bs4 import BeautifulSoup
import json
import os
import io
import random

# 如何进行一次网络访问
# 输入: 网址
# 输出: 访问后的返回数据
def webRequest(url):
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cookie':'_zap=ead10bb7-dfaf-417a-976a-a1649bd67c0b; d_c0=AECWxu_4-RWPTkEyOiseZ1fcChuEMJKARUk=|1670332617; YD00517437729195%3AWM_TID=pzzDTcaKSQpARFEQABKAYbxrhyYbVCMZ; __snaker__id=49erFF4uVjW18dOE; _xsrf=IDHlWDxDG0724CVz8TuFlTGhV4zjDaDk; captcha_session_v2=2|1:0|10:1694705430|18:captcha_session_v2|88:V0FBdys0dGFlYjg2VzBGWHdMcnlxc29FQlg3TmlBTzRJbUkzUDRkVU1ZM044am1vR2wzWTNFaHAxWHMwYWo4bA==|4f67b95e31a8d6f83943f8f2ae4f91eb9aa5edf7fd4eb8a0baedd80bf8fe7e40; gdxidpyhxdE=i%2B%5C9hqHS4kBC7EvJTBzpoR7e%2BI1IBKto2Zg55OjLSQpabGKSIhAR%2B9pfvlWWWvx%5Cg5w4lBn%5C7TEnXD4w%2Fd9d1q8kSB26Jab4zPYs7T5cjOXd%2F4yIxMERyLm9E3abIb7VC2b%2BO%2BjAuXzTBytQV2JUUPs2l6qIZ0e0xrisDUR5nEhHEoxE%3A1694706331199; YD00517437729195%3AWM_NI=7pwGR6vLRkilnhUXo017NMXfXr%2Fory1pCnIOHeZYA5xz1txYHhCp2D0%2FaaYKeS2%2Blqpe7AYfHTQJVrwRrH30nr4xhiki9LJwkXJfViomZQusom1EZeZxgVAQmwV1Xs%2BPamc%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed0c152a2b08ab8f76bacef8ba2c44b839a9b82d8729abca5aff660a39683a9b62af0fea7c3b92af5b0b9a8d13eb6949e8cec68aeb89bb9ee3cf3e982aedb6e9caee190f173f3b08d8fcc458cbb96bac43fbca6ff95fb538cb88d91b150f4f1af82dc41a78dfeccef7bb4bbf9a2dc6e8c8c9fabd57ab58ebea9b23caeaefc99eb63a9b7f7adc97da9888687d563adb396b2f879adb3ffa6d96f9aa8a9b7c45bafa99ad2db79e990af8ee237e2a3; q_c1=3c7661d57b524aaeab7c91a08e4ca198|1694705475000|1694705475000; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1693236902,1694093868,1694705430,1695187207; z_c0=2|1:0|10:1695187421|4:z_c0|92:Mi4xSVlZQ0FnQUFBQUFBUUpiRzdfajVGUmNBQUFCZ0FsVk5Rblh3WlFCN29qamd3WkhSdk9YZE9MOFJKZUFfZjA0WmR3|d052af935ef2ab60532f83a2713527bf57ebfc322e603510143e2e4512e871b9; SUBMIT_0=dbf83d92-99aa-4f2e-ba0d-98136fa68454; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1695216022; SESSIONID=4NDc0NTjyhjObO25rOJydQrdimOhgMoUqP75jYLgLqg; JOID=WlEdBUzQv-chB-oGIN5xf3f9HPE15fCtQzilU0Sm1oxgZKo1FEdB4koJ6gkvRlY9EEiIvysaMksFx099YAnqt-E=; osd=W1AUA0_Rvu4nBOsHKdhyfnb0GvI05PmrQDmkWkKl141pYqk0FU5H4UsI4w8sR1c0FkuJviIcMUoEzkl-YQjjseI=; KLBRSID=ca494ee5d16b14b649673c122ff27291|1695216033|1695216017',
        'Referer':'https://www.zhihu.com/creator/hot-question/hot/100016/hour',
        'Sec-Ch-Ua':'"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'X-Ab-Param':'',
        'X-Requested-With':'fetch',
        'X-Zse-93':'101_3_3.0',
        'X-Zse-96':'2.0_5/+v0UzOFLV2JALdoL2rTKlDH+jD6Yl1GXupoG+/9G6T1NuwRHmHMzsl5TVHu04+',
        'X-Zst-81':'3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZMXY0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPFMOMNGxYBuLqoRcOCvOYqUSYJqXBkwgYbDeY8CF0zUeYaUSLa9gY10x9ybrTvHeY2DN1dgCZAwHKwvSsqqOftB3fcwH9Q0SxfqpyG9Yf2vpqTC2sxu21mgwMr690AJL_VJOmEwgMJDVqQHXVpuF8XBOKibefTqVBPbxqsB3LsD9_CwexVqfz5CxGWbO_UC2xCgVY3JNYBvV1eweLWCHKfQxCkgC_cXe8WCt9xCwfb69M1Cps-qY1ZCwO2gNKfBpp_GYy5Bpfjcr0HwFLerXLFcf_awLGegw_QTXCqrOC'
    }
    response = requests.get(url, headers=headers)
    return response
    pass

# 解析一个json格式的数据,抽取核心问答字符串
def analysisJson(jsonString):
    # 加载一个json的字符串成为一个对象,这个对象是个字典类型
    jsonObject:dict = json.loads(jsonString)
    # 对照着json格式, 把对应的属性选择出来
    datalist = jsonObject['data']
    # 这是一种对于一个符合类型对象的数组数据的统一选取写法, 翻译成sql的话,下面这句话可以理解为 select q.question.title, q.question.url from datalist
    # 这种用法是一种方便的写法,本质上就是for循环操作,这种类似的操作学名叫做遍历
    # 具体可见: https://blog.csdn.net/weixin_39800990/article/details/110053992
    # 列表的基本操作(很常用): https://blog.csdn.net/I_r_o_n_M_a_n/article/details/115100538
    questionList = [(q['question']['title'], q['question']['url']) for q in datalist]
    # 返回的是一个列表,列表的每个元素是一个元组
    return questionList
    pass

# 解析一个html格式的数据,抽取核心问答字符串
def analysisHtml(htmlString):
    pass

# 运行的函数入口
def run():
    # 爬取的数据列表,所有爬到的数据追加到这个列表中,最后统一保存(这种方法当访问量巨大的时候会因为数据太大爆内存,应该及时存成文件,当前简化)
    result = []
    # 循环,每次爬一页20条
    for i in range(0,300,50):
        # 以探明目标网址
        # 设置这些变量是为了可以方便的通过修改变量来改为爬取其他类别网址
        # 100013 情感 100015 两性 100016 母婴 100006 教育
        domain = 100006
        skip = i
        take = 50
        period = 'week'


        hotAPISample = f'https://www.zhihu.com/api/v4/creators/rank/hot?domain={domain}&limit={take}&offset={skip}&period={period}'

        # 通过get方法访问网络请求
        # 网络请求通常有 get post两种方法,其他的方法使用的不多, 具体可以从浏览器查询
        response = webRequest(hotAPISample)
        # 将json的数据中,需要的问题和相应链接拆出来
        questions = analysisJson(response.text)

        result += questions

        time.sleep(random.random() * 3)

    # 保存结果,写入文件, 媳妇儿这里面可以直接让这些数据写入mysql数据库
    output = "/output.txt"
    # 拼接成绝对路径
    fullpathoutput = os.path.join(str(os.getcwd()), output)

    # with 用法:当有些函数的功能需要在不用的时候释放资源(比如当前打开的文件之后,需要关闭否则别的程序打不开它), 用with 括起来可以不用操心写关闭的代码,会自动走出with 的范围后调用关闭
    # 等效的写法
    # f = open(file1, mode='w')
    # xxxx 写入了一堆东西
    # f.close()
    # 可参考: https://blog.csdn.net/bradyM/article/details/125482733
    with open(file=fullpathoutput, mode='w', encoding='utf-8') as file:
        for row in result:
            # 字符串配合变量格式化的用法f
            # 可参考 https://blog.csdn.net/m0_54701273/article/details/129916943
            file.write(f'{row[0]}\t{row[1]}\r')

    pass

# 这里可以用来写一些测试功能的代码
def test():
    domain = 100016
    skip = 0
    take = 20
    period = 'week'
    hotAPISample = f'https://www.zhihu.com/api/v4/creators/rank/hot?domain={domain}&limit={take}&offset={skip}&period={period}'
    response = webRequest(hotAPISample)
    print(response.text)
    questionList = analysisJson(response.text)
    print(questionList)
    pass

# 如果当前name为main(直接运行此文件而不是给别的文件引用的情况),执行程序入口
if __name__ == "__main__":
    # test()
    run()