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
    def test():
        BaidunetdiskUtils.upload("G:/test.png", '/origin/')
        BaidunetdiskUtils.list('/origin/')


if __name__ == '__main__':
    BaidunetdiskUtils.test()
