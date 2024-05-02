from config import DB, FS
from werkzeug.utils import secure_filename

def load_n_companies(n=None):
    return list(DB['companies'].find())


def load_companies_for_student(student_id):
    student = DB['students'].find({'google_id': student_id})

    def mapper(company):
        keep = ['google_id', 'name', 'email', 'location',
                'phone', 'website', 'logo', 'description']
        res = {k: company.get(k, None) for k in keep}
        res['state'] = 'none'
        if res['google_id'] in student['accept']:
            res['state'] = 'accept'
        elif res['google_id'] in student['pending']:
            res['state'] = 'pending'
        # res['_id'] = str(company['_id'])
        return res

    return list(map(mapper, load_n_companies()))

def load_instructors_for_student(student_id):
    student = DB['students'].find({'google_id': student_id})
    def mapper(instructor):
        keep = ['google_id', 'name', 'email', 'institute',
                'avatar']
        return {k: instructor.get(k, None) for k in keep}

def load_user_raw_info(user_type, user_id):
    if user_type not in DB.list_collection_names():
        return None
    return DB[user_type].find_one({'google_id': user_id})

def load_user_info(user_type, user_id):
    res = load_user_raw_info(user_type, user_id)
    if res is not None:
        res['user_type'] = user_type
        res['_id'] = str(res['_id'])
    return res

def update_cv(student_id, file):
    file_id = FS.put(file, filename=secure_filename(file.filename))
    DB['students'].update_one({'google_id': student_id},
                              {'cv': file_id})
