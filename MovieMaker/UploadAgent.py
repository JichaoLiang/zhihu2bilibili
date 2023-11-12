import time

from bypy import ByPy

from Utils.CommonUtils import CommonUtils
import datetime


class UploadAgent:
    @staticmethod
    def pickVideo():
        pass

    @staticmethod
    def upload(videofile):
        pass

    @staticmethod
    def checkedName(videofile):
        pass

    @staticmethod
    def run():
        pickedPath = UploadAgent.pickVideo()
        try:
            CommonUtils.retry(UploadAgent.upload(pickedPath))
            UploadAgent.checkedName(pickedPath)
            print(f'upload file {pickedPath} success.')
        except Exception as ex:
            print(f"upload file {pickedPath} failed: " + str(ex))
        pass

    @staticmethod
    def process(*args):
        now = datetime.datetime.now()
        hour = now.hour
        hours = sorted(args)
        while True:
            for i in range(0, len(hours)):
                h = hours[i]
                if h == hour:
                    print("run job")
                    UploadAgent.run()
                    break
            print(f"Now: {hour}, go to sleep.")
            time.sleep(60 * 60)


if __name__ == '__main__':
    bypy = ByPy()
    paths = bypy.list('/origin/')
    for p in paths:
        print(p)
    print(paths)
    print('111')
    # UploadAgent.process(9, 13, 16)
