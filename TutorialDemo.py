import requests
from bs4 import BeautifulSoup
import json
import os
import io

# 如何进行一次网络访问
# 输入: 网址
# 输出: 访问后的返回数据
def webRequest(url):
    response = requests.get(url)
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
    for i in range(0,200,20):
        # 以探明目标网址
        # 设置这些变量是为了可以方便的通过修改变量来改为爬取其他类别网址
        domain = 100016
        skip = i
        take = 20
        period = 'week'


        hotAPISample = f'https://www.zhihu.com/api/v4/creators/rank/hot?domain={domain}&limit={take}&offset={skip}&period={period}'

        # 通过get方法访问网络请求
        # 网络请求通常有 get post两种方法,其他的方法使用的不多, 具体可以从浏览器查询
        response = webRequest(hotAPISample)
        # 将json的数据中,需要的问题和相应链接拆出来
        questions = analysisJson(response.text)

        result += questions

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