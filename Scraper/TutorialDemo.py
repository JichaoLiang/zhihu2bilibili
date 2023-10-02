import random
import time

import requests
from bs4 import BeautifulSoup
import json
import os
import io
import randomNum

# 如何进行一次网络访问
# 输入: 网址
# 输出: 访问后的返回数据
def webRequest(url):
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
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
    questionList = [(q['question']['title'], q['question']['url'], q['question']['url'].split('/')[-1]) for q in datalist]
    # 返回的是一个列表,列表的每个元素是一个元组
    return questionList
    pass

# 解析一个html格式的数据,抽取核心问答字符串
def analysisHtml(htmlString):
    pass

# 运行的函数入口
def run(domain, period='week'):
    # 爬取的数据列表,所有爬到的数据追加到这个列表中,最后统一保存(这种方法当访问量巨大的时候会因为数据太大爆内存,应该及时存成文件,当前简化)
    result = []
    # 循环,每次爬一页20条
    for i in range(0,300,50):
        # 以探明目标网址
        # 设置这些变量是为了可以方便的通过修改变量来改为爬取其他类别网址
        # 100013 情感 100015 两性 100016 母婴 100006 教育
        skip = i
        take = 50
        # period = 'week' 'day' 'hour'


        hotAPISample = f'https://www.zhihu.com/api/v4/creators/rank/hot?domain={domain}&limit={take}&offset={skip}&period={period}'

        # 通过get方法访问网络请求
        # 网络请求通常有 get post两种方法,其他的方法使用的不多, 具体可以从浏览器查询
        response = webRequest(hotAPISample)
        # 将json的数据中,需要的问题和相应链接拆出来
        questions = analysisJson(response.text)
        print(questions)
        result += questions
        time.sleep(randomNum.random01() * 3)
    return result
    pass
def save(result):

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
    result = run(100006)
    save(result)