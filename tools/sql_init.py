

import json
import pymongo
from sql_init1 import PyMySql, MongoDB
from dataCompare import DataCheck

# myclient1 = pymongo.MongoClient(
#     'mongodb://dbReadOnly:5S8PuWFIxQlTzkOp@dds-wz9bad66cc541fd41511-pub.mongodb.rds.aliyuncs.com:3717/admin')
# db = myclient1['amzViewDe'].categoryBoardView
# # for x in d:
# #     data=db.get_collection('keywordHistoryWeek').find({"_id" : x}) #查找
# data = db.find({"categoryId": "2993039031","day": "2021-10-22"}) #查找

# # 带条件查
# data=db.get_collection('categoryBoardView').count_documents({"_id" : "0001064703"})
#
# # 查总数
# data=db.get_collection('categoryBoardView').estimated_document_count()
# print(data)

conn1 = PyMySql('am-wz98fxwzhr4ue88yh90650o.ads.aliyuncs.com', 'oalur_data', 'djt8IPN2R4GFNbp8', 'oalur_data')

data1 = conn1.query("SELECT categoryId, day, list, spiderTime FROM `oalur_data`.`board_info_amz_de` WHERE `categoryId` = '2993039031' AND `day` = '2021-10-22' AND `type` = 'best-sellers' LIMIT 0,1000;")

conn2 = MongoDB('mongodb://dbReadOnly:5S8PuWFIxQlTzkOp@dds-wz9bad66cc541fd41511-pub.mongodb.rds.aliyuncs.com:3717/admin', 'amzViewDe', 'categoryBoardView' )

data2 = conn2.find({"categoryId": "2993039031", "day": "2021-10-22", "type": "best-sellers"},{"_id": 0, "type": 0})
data3 = [i for i in data2]

print(data1)
print(data3)

print(DataCheck().valuecheck("list",data1,data3,digital=True))

# PyMySql('am-wz98fxwzhr4ue88yh90650o.ads.aliyuncs.com', 'oalur_data', 'djt8IPN2R4GFNbp8', 'oalur_data')


# if __name__ == "__main__":


