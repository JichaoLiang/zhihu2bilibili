import os.path


class Config:
    localTTSSpeed = 1.0
    forceLocalTTS = True

    recalllimit = 5
    basePath = r'R:\workspace\zhihu2bilibili'
    dataPath = os.path.join(basePath, 'Resource/Data')
    voice_male_default = 'zh-CN-YunxiNeural'
    voice_female_default = 'zh-CN-XiaoyiNeural'
    tempPath = os.path.join(basePath, 'Resource/Temp')
    glmModelPath = r"J:\git\chatglmmodel"

    productPath = os.path.join(basePath, 'Resource/output')
    bgpicPath = os.path.join(basePath, 'Resource/bground.png')
    stopFlagFilePath = os.path.join(basePath, 'Resource/stop.txt')

    bilibiliCredentialPath = os.path.join(basePath, 'Resource/bilibili_credential.json')

    # 最小回答长度
    minAnswerLength = 80
    maxAnswerlength = 1000

    # 编辑会话
    hostspeech = '{question}, 一起来听听三位懂王的回答!'
    conclusionspeech = '听完了各位的回答，大家对他们的回答有什么想法呢？欢迎到评论区发出你的想法，咱们下期再见！'

    # 使用字体
    font_douyin = r"C:\Windows\Fonts\douyinmeihaoti.otf"
    font_fanti1 = "C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Windows\\Fonts\\hanyialitifan.ttf"
    font_douyu = r"C:\Users\Administrator\AppData\Local\Microsoft\Windows\Fonts\douyuzhuiguangti.ttf"
    subtitlefont = font_douyin # "C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Windows\\Fonts\\hanyialitifan.ttf"
    headerfont = font_douyu # r"C:\Users\Administrator\AppData\Local\Microsoft\Windows\Fonts\douyuzhuiguangti.ttf"

    bgmvol = 0.05

if __name__ == '__main__':
    print(os.path.abspath(Config.dataPath))
