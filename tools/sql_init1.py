import pymongo
import pymysql


MONGO_DS_PROD = 'mongodb://dbReadOnly:5S8PuWFIxQlTzkOp@dds-wz9bad66cc541fd41511-pub.mongodb.rds.aliyuncs.com:3717/admin'
host = 'am-wz98fxwzhr4ue88yh90650o.ads.aliyuncs.com',
user = 'oalur_data',
passwd = 'djt8IPN2R4GFNbp8',
db = 'oalur_data',
charset = 'utf8'
# 兼容MySQLdb
pymysql.install_as_MySQLdb()
class MongoDB:
    def __init__(self, uri='', db='', collection=''):
        """初始化MongoDB数据库和表的信息并连接数据库

        :param uri: 连接名
        :param db: 数据库名
        :param collection: 表名
        """
        client = pymongo.MongoClient(uri)
        self.db = client[db]  # 数据库
        self.collection = self.db[collection]  # 表

        if db not in client.database_names():
            print("数据库不存在！")
        if collection not in self.db.collection_names():
            print("表不存在！")

    # def __str__(self):
    #     """数据库基本信息"""
    #     db = self.db._Database__name
    #     collection = self.collection._Collection__name
    #     num = self.collection.find().count()
    #     return "数据库{} 表{} 共{}条数据".format(db, collection, num)

    def __str__(self):
        """数据库基本信息"""
        db = self.db.name
        collection = self.collection.name
        num = self.collection.find().count()
        return "数据库{} 表{} 共{}条数据".format(db, collection, num)

    def __len__(self):
        """表的数据条数"""
        return self.collection.find().count()

    def count(self):
        """表的数据条数"""
        return len(self)

    def find(self, *args, **kwargs):
        """保留原接口"""
        return self.collection.find(*args, **kwargs)

    def find_all(self, show_id=False):
        """所有查询结果

        :param show_id: 是否显示_id，默认不显示
        :return:所有查询结果
        """
        if show_id == False:
            return [i for i in self.collection.find({}, {"_id": 0})]
        else:
            return [i for i in self.collection.find({})]

    def find_col(self, *args, **kwargs):
        """查找某一列数据

        :param key: 某些字段，如"name","age"
        :param value: 某些字段匹配，如gender="male"
        :return:
        """
        key_dict = {"_id": 0}  # 不显示_id
        key_dict.update({i: 1 for i in args})
        return [i for i in self.collection.find(kwargs, key_dict)]

    def __exit__(self, *args):
        print('关闭数据库连接')
        self.client.close()

class PyMySql:
        # 初始化对象，产生一个mysql连接
        def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
            self._host = host
            self._user = user
            self._passwd = passwd
            self._db = db
            self._port = port
            self._charset = charset
            self._conn = None
            self._cursor = None
            try:
                self._conn = pymysql.connect(
                    host=self._host,
                    user=self._user,
                    password=self._passwd,
                    database=self._db,
                    charset=self._charset,
                    port=self._port,
                    autocommit=True
                )
            except Exception as err:
                format_err = f"ERROR - {self._host} mysql_session init failed: {err}" + "\n"
                raise Exception(format_err)

        # 调用with方法的入口
        def __enter__(self):
            return self

        # 调用with方法结束时启动
        def __exit__(self, exc_type, exc_val, exc_tb):
            self._conn.close()

        # 查询函数
        def query(self, sql):
            """
            :param sql: 查询语句
            :return: result-查询结果;
            """
            cursor = self._conn.cursor(pymysql.cursors.DictCursor)
            try:
                result = []
                rows = cursor.execute(sql)
                if rows > 0:
                    sql_result = cursor.fetchall()
                    # result = [list(i) for i in sql_result]
                    result = sql_result
                cursor.close()
                return result
            except Exception as err:
                format_err = f"ERROR - {self._host} query failed: {err} - {sql}" + "\n"
                raise Exception(format_err)
            finally:
                cursor.close()

        # 单条dml语句
        def change(self, sql):
            """
            :param sql: dml语句
            :return : rows-改动的记录条数
            """
            cursor = self._conn.cursor()
            try:
                rows = cursor.execute(sql)
                return rows
            except Exception as err:
                format_err = f"ERROR - {self._host} change failed: {err} - {sql}" + "\n"
                raise Exception(format_err)
            finally:
                cursor.close()

        # 多条dml语句
        def change_many(self, sql, value_list):
            """
            :param sql: 修改语句
            :param value_list: 参数值列表
            :return:rows-改动的记录条数
            """
            cursor = self._conn.cursor()
            try:
                rows = cursor.executemany(sql, value_list)
                return rows
            except Exception as err:
                format_err = f"ERROR - {self._host} change_many failed: {err} - {sql}" + "\n"
                raise Exception(format_err)
            finally:
                cursor.close()


if __name__ == '__main__':
    # print(MongoDB(MONGO_DS_PROD, 'amzViewDe', 'stopWords').count())
    # dd = PyMySql('am-wz98fxwzhr4ue88yh90650o.ads.aliyuncs.com', 'oalur_data', 'djt8IPN2R4GFNbp8', 'oalur_data')
    # data = dd.query("SELECT * FROM `oalur_data`.`board_info_amz_de` WHERE `categoryId` = '2993039031' AND `day` = '2021-10-22' LIMIT 0,1000;")
    # print(data)
    def is_toJson(str):
        """判断能否转化为列表"""
        a = "[{'shareOtd': '2.00', 'shareFrz': 'test'},{'shareOtd': '0.00', 'shareFrz': 'adbv'},]"
        b = "1011re"
        c = '{"loanDate": "2020/05/07", "day": "4", "moneyUseDate": "2020/05/11", "moneyTakeDate": "2020/05/12"}'
        try:
            eval(str)
        except:
            return False
        return True


    a = "[{'shareOtd': '2.00', 'shareFrz': 'test'},{'shareOtd': '0.00', 'shareFrz': 'adbv'},]"
    b = "1011re"
    c = '{"loanDate": "2020/05/07", "day": "4", "moneyUseDate": "2020/05/11", "moneyTakeDate": "2020/05/12"}'
    print(is_toJson(a),is_toJson(b),is_toJson(c))
    print(str("a"))