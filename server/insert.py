from pymongo import MongoClient

from server.config import DB


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
    "name": "Disney",
    "email": "disneyinfo@gmail.com",
    "password": "12345678",
    "user_type":"companies",
    "description":"good good good",
    "location":'USA',
    "pending":["alice@vub.be","aaa@vub.be","wangshifu@vub.be"],
    "accepted":["ziz@gmail.com"],
}


# result = DB.students.insert_one(new_data)
result = DB.companies.insert_one(new_data)
result2 = DB.users.insert_one(new_data)

print("Data inserted with id:", result2.inserted_id)
