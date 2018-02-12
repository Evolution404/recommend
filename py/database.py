from pymongo import MongoClient

client = MongoClient()

db = client['图书馆']
data = db['data']
if(not data.find_one({'id':'1'})):

    cursor = data.insert_one(
        {
            'id': '3',
            'name': '333'
        }
    )
    print('插入成功')
else:
    print('重复')