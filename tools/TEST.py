import json
import pymysql
from elasticsearch import Elasticsearch

def TableToJson():
    # 连接数据库
    conn = pymysql.connect(
            host='am-wz98fxwzhr4ue88yh90650o.ads.aliyuncs.com',
            user='oalur_data',
            password='djt8IPN2R4GFNbp8',
            db='oalur_data',
            charset='utf8'
        )
    # 建立游标cursor
    cursor = conn.cursor()
    # 执行查
    cursor.execute("SELECT * FROM `oalur_data`.`comments_amz_uk` WHERE `asin` = 'B073XHBD84' AND `date` >= '2021-05-14' AND `date` <= '2022-05-14' LIMIT 0,1000;")
    # 查询数据库多条数据
    result = cursor.fetchall()
    fields = cursor.description
    cursor.close()
    conn.close()

    # 定义字段名的列表
    column_list = []
    for i in fields:
        column_list.append(i[0])

    # 打开输出结果文件
    with open('./json.txt', 'w+') as f:
        # 一次循环，row代表一行，row以元组的形式显示
        for row in result:
            # 定义Python 字典
            data = {}
            # 将row中的每个元素，追加到字典中。
            for i in range(len(column_list)):
                data[column_list[i]] = row[i]
            jsondata = json.dumps(data,ensure_ascii=False)
            # 写入文件
            f.write(jsondata + '\n')
    f.close()

def connect_xianshang_es():
    ip = 'es-cn-mp91a4gpq000bdk5x.public.elasticsearch.aliyuncs.com'
    es = Elasticsearch([ip], http_auth=('meiyongsheng', 'oalur1607'), port=9200)
    # 字段形式设置es查询body,根据相应的索引进行查询
    b = {
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "asin.keyword": {
              "value": "B073XHBD84"
            }
          }
        },
        {
          "range": {
            "date": {
              "gte": "2021-05-14",
              "lte": "2022-05-14"
            }
          }
        }
      ]
    }
  },
  "size": 1000
}
    data = es.search(index="ukcomments", doc_type='slice', body=b)
    hits_value = data['hits']
    # 打印查询结果
    # print(source1)
    return hits_value

def compare():
    hits_value = connect_xianshang_es()
    for i in range(len(hits_value['hits'])):
        es_id = hits_value['hits'][i]['_source']['id']
        id1 = hits_value['hits'][i]['_source']['id']
        TableToJson()
        with open('./json.txt', 'r', encoding='utf-8') as rfile:
            student = rfile.readlines()
            for item in student:
                d = json.loads(item)

                # 格式转化
                if d['isVineVoice'] == 0:
                    d['isVineVoice'] = False
                elif d['isVineVoice'] == 1:
                    d['isVineVoice'] = True
                elif d['isVineVoice'] == None:
                    pass
                else:
                    print('isVineVoice有误')
                if d['attributes'] == None:
                    d['attributes'] = []
                else:
                    attributes = d['attributes']
                    dict_attributes = json.loads(attributes)
                    d['attributes'] = [{'key':'Size','value':dict_attributes['Size']}]
                if d['imgs'] == None:
                    d['imgs'] = []
                else:
                    imgs = d['imgs']
                    list_imgs = json.loads(imgs)
                    d['imgs'] = list_imgs
                if d['videos'] == None:
                    d['videos'] = []
                else:
                    videos = d['videos']
                    list_videos = json.loads(videos)
                    d['videos'] = list_videos
                if d['purchased'] == 0:
                    d['purchased'] = False
                elif d['purchased'] == 1:
                    d['purchased'] = True
                else:
                    print('purchased有误')
                a = d['spiderTime']
                d['spiderTime'] = {'$numberLong': str(a)}

                count = 0
                if d['id'] == id1:
                    print(d)
                    print(hits_value['hits'][i]['_source'])
                    if d == hits_value['hits'][i]['_source']:
                        print('数据一致')
                    else:
                        print('数据不一致')

if __name__ == '__main__':
    compare()



