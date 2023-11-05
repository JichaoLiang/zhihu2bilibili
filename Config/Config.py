import os.path


class Config:
    recalllimit = 5
    dataPath = os.path.abspath('../Resource/Data')
    voice_male_default = 'zh-CN-YunxiNeural'
    voice_female_default = 'zh-CN-XiaoyiNeural'
    tempPath = os.path.abspath('../Resource/Temp')

    productPath = os.path.abspath('../Resource/output')
    bgpicPath = os.path.abspath('../Resource/bground.png')
    stopFlagFilePath = os.path.abspath('../Resource/stop.txt')

    bilibiliCredentialPath = os.path.abspath('../Resource/bilibili_credential.json')

    # 最小回答长度
    minAnswerLength = 80
    maxAnswerlength = 1000

    # 编辑会话
    hostspeech = '{question}, 我精心挑选了三个热心网友回答，大家看看谁聊得更精彩，那么咱们现在开始吧！'
    conclusionspeech = '听完了各位的回答，大家对他们的回答有什么想法呢？欢迎到评论区发出你的想法，咱们下期再见！'

    # 使用字体
    font_douyin = r"C:\Windows\Fonts\douyinmeihaoti.otf"
    font_fanti1 = "C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Windows\\Fonts\\hanyialitifan.ttf"
    font_douyu = r"C:\Users\Administrator\AppData\Local\Microsoft\Windows\Fonts\douyuzhuiguangti.ttf"
    subtitlefont = font_douyin # "C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Windows\\Fonts\\hanyialitifan.ttf"
    headerfont = font_douyu # r"C:\Users\Administrator\AppData\Local\Microsoft\Windows\Fonts\douyuzhuiguangti.ttf"

    bgmvol = 0.3

if __name__ == '__main__':
    print(os.path.abspath(Config.dataPath))
