import os

from bilibili_api import rank, sync, Credential, video_uploader

import Config.Config
import Utils.CommonUtils
import json

from Utils.MovieMakerUtils import MovieMakerUtils


class BilibiliUtils:
    buvid4 = "706433CF-3061-92ED-DB8D-237C4B9DC76208403-022012118-QyP6TZ8JcMrJX2dzKSKyIA%3D%3D"

    @staticmethod
    def Test():
        print(sync(rank.get_rank()))
        pass

    @staticmethod
    def loadCredentialData():
        credentialData = json.loads(
            Utils.CommonUtils.CommonUtils.readAllText(Config.Config.Config.bilibiliCredentialPath))
        sessdata = credentialData["sessdata"]
        bili_jct = credentialData["bili_jct"]
        buvid3 = credentialData["buvid3"]
        buvid4 = credentialData["buvid4"]
        ac_time_value = credentialData["ac_time_value"]
        return sessdata, bili_jct, buvid3, buvid4, ac_time_value
        pass

    @staticmethod
    def saveCredentialData(sessdata, bili_jct, buvid3, ac_time_value, buvid4):
        buildData = {
            "sessdata": sessdata,
            "bili_jct": bili_jct,
            "buvid3": buvid3,
            "ac_time_value": ac_time_value,
            "buvid4": buvid4
        }
        jsondata = json.dumps(buildData)
        print(jsondata)
        Utils.CommonUtils.CommonUtils.writeAllText(Config.Config.Config.bilibiliCredentialPath, jsondata)
        pass

    @staticmethod
    def getCredential():
        sessdata, bili_jct, buvid3, buvid4, ac_time = BilibiliUtils.loadCredentialData()
        credential = Credential(
            sessdata=sessdata,
            bili_jct=bili_jct, buvid3=buvid3,
            ac_time_value=ac_time)
        needrefresh = sync(credential.check_refresh())
        if needrefresh:
            sync(credential.refresh())
            newsessdata = credential.sessdata
            newbilijct = credential.bili_jct
            newbuvid3 = credential.buvid3
            newactime = credential.ac_time_value
            BilibiliUtils.saveCredentialData(newsessdata, newbilijct, newbuvid3, newactime, buvid4)
        return credential
    @staticmethod
    def Upload_sync(videoPath, title=None, desc=None, cover=None):
        credential = BilibiliUtils.getCredential()
        sync(BilibiliUtils.Upload(videoPath=videoPath, title=title, desc=desc, cover=cover, credential=credential))
        pass

    @staticmethod
    async def Upload(videoPath, title=None, desc=None, cover=None, credential=None, tags=[]):
        filename = os.path.basename(videoPath)
        fileprimaryname = filename.split('.')[0]
        if title is None:
            title = fileprimaryname
        if desc is None:
            desc = fileprimaryname
        if cover is None:
            cover = MovieMakerUtils.getCaptureFile(videoPath, momentSec=0.5)
        # 具体请查阅相关文档
        meta = {
            "act_reserve_create": 0,
            "copyright": 1,
            "source": "",
            "desc": desc,
            "desc_format_id": 9999,
            "dynamic": "",
            "interactive": 0,
            "no_reprint": 1,
            "open_elec": 0,
            "origin_state": 0,
            "subtitles": {
                "lan": "",
                "open": 0
            },
            "tag": ",".join(tags),
            "tid": 130,
            "title": title,
            "up_close_danmaku": False,
            "up_close_reply": False,
            "up_selection_reply": False,
            "dtime": 0
        }
        page = video_uploader.VideoUploaderPage(path=videoPath, title=title, description=desc)
        uploader = video_uploader.VideoUploader([page], meta, credential, cover=cover)

        @uploader.on("__ALL__")
        async def ev(data):
            print(data)

        await uploader.start()
        pass


if __name__ == '__main__':
    pathfile = r'g:/一个有教养的女生是什么样的？.mp4'
    BilibiliUtils.Upload_sync(pathfile)
