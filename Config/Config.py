import os.path


class Config:
    dataPath = os.path.abspath('../Resource/Data')
    voice_male_default = 'zh-CN-YunxiNeural'
    voice_female_default = 'zh-CN-XiaoyiNeural'
    tempPath = os.path.abspath('../Resource/Temp')

    productPath = os.path.abspath('../Resource/output')



if __name__ == '__main__':
    print(os.path.abspath(Config.dataPath))
