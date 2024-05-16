from pymongo import MongoClient

from server.config import DB

# 要插入的数据
# new_data = {
#     "name": "ming",
#     "email": "ming@vub.be",
#     "password": "12345678",
#     "institute": "vub",
#     "instructors": ["wow", "wow2"],
#     "pending": ["google@gmail.com", "facebook@gmail.com"],
#     "accepted": [""],
#     "user_type":"students",
#     "cv":"",
#
# }

new_data = {
    "name": "apple",
    "email": "appleinfo@gmail.com",
    "password": "12345678",
    "user_type":"companies",
    "description":"good good good",
    "location":'USA',
    "pending":[],
    "accepted":[],
}

# 插入数据
# result = DB.students.insert_one(new_data)
result = DB.companies.insert_one(new_data)
result2 = DB.users.insert_one(new_data)
# 打印插入结果
print("Data inserted with id:", result2.inserted_id)
