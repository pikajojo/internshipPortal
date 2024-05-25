from config import DB, FS
from werkzeug.utils import secure_filename
from bson import ObjectId
from io import BytesIO

def load_all_companies(n=None):
    return list(DB['companies'].find())


# def load_companies_for_student(student_id):
#     student = DB['students'].find_one({'email': student_id})
#
#     def mapper(company):
#         keep = ['name', 'email', 'location',
#                 'phone', 'website', 'logo', 'description']
#         res = {k: company.get(k, None) for k in keep}
#         res['state'] = 'none'
#         if res['email'] in student['accepted']:
#             res['state'] = 'accept'
#         elif res['email'] in student['pending']:
#             res['state'] = 'pending'
#         # res['_id'] = str(company['_id'])
#         return res
#
#     return list(map(mapper, load_all_companies()))


def load_companies_for_student(student_id):
    student = DB['students'].find_one({'email': student_id})

    def mapper(company):
        keep = ['google_id','name', 'email', 'location', 'phone', 'website', 'logo', 'description']
        res = {k: company.get(k, None) for k in keep}
        res['state'] = 'none'  # 默认状态为 apply

        if res['email'] in student.get('accepted', []):
            res['state'] = 'accept'
        elif res['email'] in student.get('pending', []):
            res['state'] = 'pending'

        return res

    all_companies = list(DB['companies'].find())  # 获取所有公司
    return list(map(mapper, all_companies))


def load_instructors_for_student(student_id):
    student = DB['students'].find_one({'email': student_id})

    def mapper(instructor):
        keep = ['name', 'email', 'institute',
                'avatar']
        return {k: instructor.get(k, None) for k in keep}


def load_user_raw_info(user_type, user_id):
    if user_type not in DB.list_collection_names():
        return None
    return DB[user_type].find_one({'email': user_id})


def load_user_info(user_type, user_id):
    res = load_user_raw_info(user_type, user_id)
    if res is not None:
        res['user_type'] = user_type
        res['_id'] = str(res['_id'])
    return res


def update_cv(student_id, file, filename):
    file_id = FS.put(file, filename=secure_filename(filename))
    DB['students'].update_one({'email': student_id},
                              {'$set': {'cv': str(file_id)}})


def update_institute(student_id, institute_name):
    try:
        # Update the student's institute in the database
        DB['students'].update_one(
            {'email': student_id},
            {'$set': {'institute': institute_name}}
        )
        return True
    except Exception as e:
        print(f"Error updating institute: {e}")
        return False


def update_major(student_id, major_name):
    try:
        # Update the student's major in the database
        DB['students'].update_one(
            {'email': student_id},
            {'$set': {'major': major_name}}
        )
        return True
    except Exception as e:
        print(f"Error updating major: {e}")
        return False


def load_file(file_id):
    grid_file = FS.get(ObjectId(file_id))
    bio = BytesIO(grid_file.read())
    bio.seek(0)
    return bio, grid_file.filename


def load_students_for_company(company_id, state):
    def mapper(student_id):
        student_info = DB['students'].find_one({'email': student_id})
        if student_info is None:
            return None
        keep = ['name', 'email', 'institute',
                'cv', 'avatar']
        return {k: student_info.get(k, None) for k in keep}

    company_info = DB.companies.find_one({'email': company_id})
    if company_info is None:
        return None
    # if state not in company_info:
    #     return None
    return list(map(mapper, company_info[state]))
