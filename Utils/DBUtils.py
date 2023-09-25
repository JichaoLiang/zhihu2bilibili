import pymysql

class DBUtils:
    @staticmethod
    def test():
        pass

    def __init__(self):
        pass

    connection = None

    def tryConnect(self):
        if self.connection is None:
            self.connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='tk1372353',
                db='zhihu2bilibili',
                charset='utf8',
            )
        return self.connection

    def doQuery(self, sql):
        connect = self.tryConnect()
        with connect.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    def doCommand(self, sql):
        connect = self.tryConnect()
        with connect.cursor() as cursor:
            cursor.execute(sql)
        connect.commit()

    pass

if __name__ == '__main__':
    DBUtils.test()