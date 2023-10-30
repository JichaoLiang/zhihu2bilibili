from bypy import ByPy
class BaidunetdiskUtils:
    @staticmethod
    def upload(filepath):
        baidunetdiskclient = ByPy()
        baidunetdiskclient.upload(filepath)
    @staticmethod
    def list():
        baidunetdiskclient = ByPy()
        list = baidunetdiskclient.list()
        print(list)

    @staticmethod
    def test():
        BaidunetdiskUtils.upload("G:/test/opening_o.mp4")
        BaidunetdiskUtils.list()

if __name__ == '__main__':
    BaidunetdiskUtils.test()