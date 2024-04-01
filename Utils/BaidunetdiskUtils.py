import os.path

from bypy import ByPy

from Config.Config import Config
from Utils.CommonUtils import CommonUtils


class BaidunetdiskUtils:
    @staticmethod
    def upload(filepath, dest='/'):
        baidunetdiskclient = ByPy()
        baidunetdiskclient.upload(filepath, dest)

    @staticmethod
    def list(path='/'):
        baidunetdiskclient = ByPy()
        list = baidunetdiskclient.list(path)
        print(list)

    @staticmethod
    def sync(relpath='/task/'):
        baidunetdiskclient = ByPy()
        baidunetdiskclient.syncdown(relpath, os.path.join(Config.basePath, f'Resource/baidunetdisk{relpath}'), True)

    @staticmethod
    def syncUp(relpath='/task/'):
        baidunetdiskclient = ByPy()
        baidunetdiskclient.syncup(relpath, os.path.join(Config.basePath, f'Resource/baidunetdisk{relpath}'), True)

    @staticmethod
    def popSearchTaskQueue() -> list:
        taskpath = os.path.join(Config.basePath, f'Resource/baidunetdisk/task/task.txt')
        BaidunetdiskUtils.sync()
        lines = CommonUtils.readAllText(taskpath).split('\n')
        if lines.__contains__(''):
            lines.remove('')
        client = ByPy()
        client.remove('/task/task.txt')
        BaidunetdiskUtils.newTaskFile()
        return lines
        pass

    @staticmethod
    def newTaskFile():
        client = ByPy()
        taskpath = os.path.join(Config.basePath, f'Resource/baidunetdisk/task/task.txt')
        if os.path.exists(taskpath):
            os.remove(taskpath)
        CommonUtils.writeAllText(taskpath, '')
        client.upload(taskpath, 'task/task.txt')

    @staticmethod
    def test():
        # BaidunetdiskUtils.sync()
        queue = BaidunetdiskUtils.popSearchTaskQueue()
        print(queue)


if __name__ == '__main__':
    BaidunetdiskUtils.test()
