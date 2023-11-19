from bypy import ByPy


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
    def searchTaskQueue()->list:
        pass

    @staticmethod
    def setSearchTaskQueue(queue:list):
        pass

    @staticmethod
    def popSearchTaskQueue(limit=5):
        taskQueue =

    @staticmethod
    def test():
        BaidunetdiskUtils.upload("G:/test.png", '/origin/')
        BaidunetdiskUtils.list('/origin/')


if __name__ == '__main__':
    BaidunetdiskUtils.test()
