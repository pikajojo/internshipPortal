from pymongo import MongoClient

from server.config import DB

# 要插入的数据
new_data = {
    "name": "john",
    "email": "john@vub.be",
    "password": "12345678",
    "institute": "vub",
    "instructors": ["daniel@vub.be"],
    "pending": ["google@gmail.com", "facebook@gmail.com"],
    "accepted": [""],
    "user_type":"students",
    "cv":"",

}

# new_data = {
#     "name": "Disney",
#     "email": "disneyinfo@gmail.com",
#     "password": "12345678",
#     "user_type":"companies",
#     "description":"good good good",
#     "location":'USA',
#     "pending":["alice@vub.be","aaa@vub.be","wangshifu@vub.be"],
#     "accepted":["ziz@gmail.com"],
# }

# new_data = {
#     "name": "Daniel",
#     "email": "daniel@vub.be",
#     "password": "12345678",
#     "user_type":"instructors",
#     "institute":"VUB",
#     "major":'Computer Science',
#     "pending":["alice@vub.be","aaa@vub.be","wangshifu@vub.be"],
#     "reviewed":["ziz@gmail.com"],
# }

# 插入数据
# result = DB.students.insert_one(new_data)
# result = DB.companies.insert_one(new_data)
result = DB.instructors.insert_one(new_data)
result2 = DB.users.insert_one(new_data)
# 打印插入结果
print("Data inserted with id:", result2.inserted_id)
