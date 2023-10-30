import os.path


class Config:
    recalllimit = 5
    dataPath = os.path.abspath('../Resource/Data')
    voice_male_default = 'zh-CN-YunxiNeural'
    voice_female_default = 'zh-CN-XiaoyiNeural'
    tempPath = os.path.abspath('../Resource/Temp')

    productPath = os.path.abspath('../Resource/output')
    bgpicPath = os.path.abspath('../Resource/bground.png')

    # 最小回答长度
    minAnswerLength = 30
    maxAnswerlength = 1000

    hostspeech = '{question}, 我精心挑选了三个热心网友回答，大家看看谁聊得更精彩，那么咱们现在开始吧！'
    conclusionspeech = '听完了各位的回答，大家对他们的回答有什么想法呢？欢迎到评论区发出你的想法，咱们下期再见！'

if __name__ == '__main__':
    print(os.path.abspath(Config.dataPath))
