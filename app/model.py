from mongoengine import Document, StringField, EmailField, URLField

# 连接到MongoDB
#connect('your_db_name')


class User(Document):
    meta = {'allow_inheritance': True}
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = EmailField(required=True)
    phone = StringField(required=True)
    role = StringField(required=True)


class Company(User):
    name = StringField(required=True)
    description = StringField(required=True)
    address = StringField(required=True)
    industry = StringField(required=True)
    website = URLField()


class Student(User):
    name = StringField(required=True)
    introduction = StringField(required=True)
    skills = StringField(required=True)
    education = StringField(required=True)





# 示例：创建一个公司
#EX:create a new company
company2 = Company(
    username='company2',
    password='youarethebest',
    user_type='company',
    name='Company Two',
    description='This is Company Two.',
    address='123 Business Ave, Metropolis',
    industry='Technology',
    email='contact@companytwo.com',
    phone='123-456-7890',
    website='https://www.companytwo.com'
)
company2.save()

# 示例：创建一个学生
#EX:create a new student
student = Student(
    username='student1',
    password='iloveprogramming',
    user_type='student',
    name='john doe',
    description='hard working, creative and quick learner.',
    address='VUB',
    major='CS',
    email='contact@vub.be',
    phone='123-456-7890',
)
student.save()
