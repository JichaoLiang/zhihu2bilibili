from Utils.CommonUtils import CommonUtils


class VoiceModel:

    voicelist = [{'Locale': 'zh-HK', 'Gender': 'Female', 'ShortName': 'zh-HK-HiuGaaiNeural',
                  'FriendlyName': 'Microsoft HiuGaai Online (Natural) - Chinese (Cantonese Traditional)'},
                 {'Locale': 'zh-HK', 'Gender': 'Female', 'ShortName': 'zh-HK-HiuMaanNeural',
                  'FriendlyName': 'Microsoft HiuMaan Online (Natural) - Chinese (Hong Kong)'},
                 {'Locale': 'zh-HK', 'Gender': 'Male', 'ShortName': 'zh-HK-WanLungNeural',
                  'FriendlyName': 'Microsoft WanLung Online (Natural) - Chinese (Hong Kong)'},
                 {'Locale': 'zh-CN', 'Gender': 'Female', 'ShortName': 'zh-CN-XiaoxiaoNeural',
                  'FriendlyName': 'Microsoft Xiaoxiao Online (Natural) - Chinese (Mainland)'},
                 {'Locale': 'zh-CN', 'Gender': 'Female', 'ShortName': 'zh-CN-XiaoyiNeural',
                  'FriendlyName': 'Microsoft Xiaoyi Online (Natural) - Chinese (Mainland)'},
                 {'Locale': 'zh-CN', 'Gender': 'Male', 'ShortName': 'zh-CN-YunjianNeural',
                  'FriendlyName': 'Microsoft Yunjian Online (Natural) - Chinese (Mainland)'},
                 {'Locale': 'zh-CN', 'Gender': 'Male', 'ShortName': 'zh-CN-YunxiNeural',
                  'FriendlyName': 'Microsoft Yunxi Online (Natural) - Chinese (Mainland)'},
                 {'Locale': 'zh-CN', 'Gender': 'Male', 'ShortName': 'zh-CN-YunxiaNeural',
                  'FriendlyName': 'Microsoft Yunxia Online (Natural) - Chinese (Mainland)'},
                 {'Locale': 'zh-CN', 'Gender': 'Male', 'ShortName': 'zh-CN-YunyangNeural',
                  'FriendlyName': 'Microsoft Yunyang Online (Natural) - Chinese (Mainland)'},
                 {'Locale': 'zh-CN-liaoning', 'Gender': 'Female', 'ShortName': 'zh-CN-liaoning-XiaobeiNeural',
                  'FriendlyName': 'Microsoft Xiaobei Online (Natural) - Chinese (Northeastern Mandarin)'},
                 {'Locale': 'zh-TW', 'Gender': 'Female', 'ShortName': 'zh-TW-HsiaoChenNeural',
                  'FriendlyName': 'Microsoft HsiaoChen Online (Natural) - Chinese (Taiwan)'},
                 {'Locale': 'zh-TW', 'Gender': 'Male', 'ShortName': 'zh-TW-YunJheNeural',
                  'FriendlyName': 'Microsoft YunJhe Online (Natural) - Chinese (Taiwan)'},
                 {'Locale': 'zh-TW', 'Gender': 'Female', 'ShortName': 'zh-TW-HsiaoYuNeural',
                  'FriendlyName': 'Microsoft HsiaoYu Online (Natural) - Chinese (Taiwanese Mandarin)'},
                 {'Locale': 'zh-CN-shaanxi', 'Gender': 'Female', 'ShortName': 'zh-CN-shaanxi-XiaoniNeural',
                  'FriendlyName': 'Microsoft Xiaoni Online (Natural) - Chinese (Zhongyuan Mandarin Shaanxi)'}]

    zh_HK_HiuGaaiNeural = {'Locale': 'zh-HK', 'Gender': 'Female', 'ShortName': 'zh-HK-HiuGaaiNeural',
                           'FriendlyName': 'Microsoft HiuGaai Online (Natural) - Chinese (Cantonese Traditional)'}
    zh_HK_HiuMaanNeural = {'Locale': 'zh-HK', 'Gender': 'Female', 'ShortName': 'zh-HK-HiuMaanNeural',
                           'FriendlyName': 'Microsoft HiuMaan Online (Natural) - Chinese (Hong Kong)'}
    zh_HK_WanLungNeural = {'Locale': 'zh-HK', 'Gender': 'Male', 'ShortName': 'zh-HK-WanLungNeural',
                           'FriendlyName': 'Microsoft WanLung Online (Natural) - Chinese (Hong Kong)'}
    zh_CN_XiaoxiaoNeural = {'Locale': 'zh-CN', 'Gender': 'Female', 'ShortName': 'zh-CN-XiaoxiaoNeural',
                            'FriendlyName': 'Microsoft Xiaoxiao Online (Natural) - Chinese (Mainland)'}
    zh_CN_XiaoyiNeural = {'Locale': 'zh-CN', 'Gender': 'Female', 'ShortName': 'zh-CN-XiaoyiNeural',
                          'FriendlyName': 'Microsoft Xiaoyi Online (Natural) - Chinese (Mainland)'}
    zh_CN_YunjianNeural = {'Locale': 'zh-CN', 'Gender': 'Male', 'ShortName': 'zh-CN-YunjianNeural',
                           'FriendlyName': 'Microsoft Yunjian Online (Natural) - Chinese (Mainland)'}
    zh_CN_YunxiNeural = {'Locale': 'zh-CN', 'Gender': 'Male', 'ShortName': 'zh-CN-YunxiNeural',
                         'FriendlyName': 'Microsoft Yunxi Online (Natural) - Chinese (Mainland)'}
    zh_CN_YunxiaNeural = {'Locale': 'zh-CN', 'Gender': 'Male', 'ShortName': 'zh-CN-YunxiaNeural',
                          'FriendlyName': 'Microsoft Yunxia Online (Natural) - Chinese (Mainland)'}
    zh_CN_YunyangNeural = {'Locale': 'zh-CN', 'Gender': 'Male', 'ShortName': 'zh-CN-YunyangNeural',
                           'FriendlyName': 'Microsoft Yunyang Online (Natural) - Chinese (Mainland)'}
    zh_CN_liaoning_XiaobeiNeural = {'Locale': 'zh-CN-liaoning', 'Gender': 'Female',
                                    'ShortName': 'zh-CN-liaoning-XiaobeiNeural',
                                    'FriendlyName': 'Microsoft Xiaobei Online (Natural) - Chinese (Northeastern Mandarin)'}
    zh_TW_HsiaoChenNeural = {'Locale': 'zh-TW', 'Gender': 'Female', 'ShortName': 'zh-TW-HsiaoChenNeural',
                             'FriendlyName': 'Microsoft HsiaoChen Online (Natural) - Chinese (Taiwan)'}
    zh_TW_YunJheNeural = {'Locale': 'zh-TW', 'Gender': 'Male', 'ShortName': 'zh-TW-YunJheNeural',
                          'FriendlyName': 'Microsoft YunJhe Online (Natural) - Chinese (Taiwan)'}
    zh_TW_HsiaoYuNeural = {'Locale': 'zh-TW', 'Gender': 'Female', 'ShortName': 'zh-TW-HsiaoYuNeural',
                           'FriendlyName': 'Microsoft HsiaoYu Online (Natural) - Chinese (Taiwanese Mandarin)'}
    zh_TW_HsiaoYuNeural = {'Locale': 'zh-CN-shaanxi', 'Gender': 'Female', 'ShortName': 'zh-CN-shaanxi-XiaoniNeural',
                           'FriendlyName': 'Microsoft Xiaoni Online (Natural) - Chinese (Zhongyuan Mandarin Shaanxi)'}

    default_male = zh_CN_YunxiNeural
    default_female = zh_CN_XiaoyiNeural

    @staticmethod
    def randomVoice(isMale):
        malelist = [item for item in VoiceModel.voicelist if item['Gender'].lower() == 'male']
        femalelist= [item for item in VoiceModel.voicelist if item['Gender'].lower() == 'female']

        list = femalelist
        if isMale:
            list = malelist
        randIndex = int(CommonUtils.random01() * len(list))
        return list[randIndex]['ShortName']
        pass
