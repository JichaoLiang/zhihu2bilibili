import os.path


class Config:
    dataPath = '../Resource/Data'
    voice_male_default = 'zh-CN-YunxiNeural'
    voice_female_default = 'zh-CN-XiaoyiNeural'



if __name__ == '__main__':
    print(os.path.abspath(Config.dataPath))
