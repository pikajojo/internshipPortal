import os
import requests
import tempfile

import werkzeug
from dotenv import load_dotenv
from flask import Flask, Response, request, jsonify, session, abort, redirect, make_response, send_file
from flask import Flask, request, send_file, jsonify
import io
from flask_session import Session
from auth import verify_user, login_required, user_required
from config import MONGODB_CLIENT, DB
import db_utils
import bcrypt




app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.config['SESSION_TYPE'] = "mongodb"
app.config['SESSION_MONGODB'] = MONGODB_CLIENT
#app.config['SESSION_MONGODB_DB'] = os.getenv("MONGODB_DB")
app.config['SESSION_MONGODB_DB'] = "apc"
#app.config['SESSION_MONGODB_COLLECTION'] = os.getenv("SESSION_MONGODB_COLLECTION")
app.config['SESSION_MONGODB_COLLECTION'] = "sessions"
Session(app)


@app.get('/api/whoami')
def whoami():
    if session['email'] is not None:
        return jsonify(db_utils.load_user_info(session['user_type'], session['email'])), 200
    return jsonify({}), 200


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    user_type = data['user_type']
    # 检查数据库中是否存在相同的用户名或邮箱
    if DB.users.find_one({"$or": [{"username": username}, {"email": email}]}):
        return jsonify({'status': 'error', 'message': 'User already exists'})

    # 用户不存在, 可以进行注册
    # password = data['password'].encode('utf-8')
    # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    #hashed = werkzeug.security.generate_password_hash(password)
    #data['password'] = hashed


    result = DB.users.insert_one(data)

    if result.inserted_id:
        if user_type == 'students':
            DB.students.insert_one(data)
        elif user_type == 'companies':
            DB.companies.insert_one(data)
        elif user_type == 'instructors':
            DB.instructors.insert_one(data)

        return jsonify({'status': 'success', 'message': 'Registration successful'})
    else:
        return jsonify({'status': 'error', 'message': 'Registration failed'})


@app.post('/api/login')
def login():
    data = request.get_json()
    user = DB.users.find_one({'email': data['email']})
    print(f"Received data: {data}")
    print(f"Found user: {user}")

    # if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
    if user and data['password'] == user['password']:
        session['email'] = user['email']
        session['user_type'] = user['user_type']
        print(session['email'])
        print(session['user_type'])
        # 在这里将 data 作为返回的 JSON 数据的一部分
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': data  # 将 data 包含在返回的 JSON 中
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid username or password'
        }), 401



@app.post('/api/logout')
def logout():
    session.pop('email')
    session.pop('user_type')
    return jsonify({}), 200


@app.post('/api/students/edit')
@user_required(user_type='students')
def students_edit():
    student_id = session.get('email')
  #  if 'file' not in request.files:
    if 'file' not in request.files and not all(k in request.form for k in ['institute', 'major']):
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    institute = request.form['institute']
    major = request.form['major']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the file to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        with open(temp_file.name, 'rb') as f:
            content = f.read()

        db_utils.update_cv(student_id, content, file.filename)
        db_utils.update_institute(student_id, institute)
        db_utils.update_major(student_id, major)
        os.unlink(temp_file.name)

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.get('/api/students/companies')
@user_required(user_type='students')
def students_companies():
    companies = db_utils.load_companies_for_student(session.get('email'))
    # companies = db_utils.load_all_companies(session.get('email'))
    return jsonify(companies), 200


@app.get('/api/students/instructors')
@user_required(user_type='students')
def students_instructors():
    instructors = db_utils.load_instructors_for_student(session.get('email'))
    return jsonify(instructors), 200


@app.post('/api/students/apply')
@user_required(user_type='students')
def students_apply():
    student_id = session.get('email')
    student_query = {'email': student_id}
    student_info = DB.students.find_one(student_query)
    if student_info['cv'] is None:
        return "No CV found", 400
    company_id = request.json.get('company_id')
    company_query = {'email': company_id}
    company_info = DB.companies.find_one(company_query)
    if ((company_info is None)
            or (student_id in company_info['pending'])
            or (student_id in company_info['accepted'])):
        abort(400)
    DB.students.update_one(student_query, {"$addToSet": {'pending': company_id}})
    DB.companies.update_one(company_query, {"$addToSet": {'pending': student_id}})

    return "Succeed", 200


@app.get('/api/companies/pending')
@user_required(user_type='companies')
def companies_pending():
    company_id = session.get('email')
    pending = db_utils.load_students_for_company(company_id, 'pending')
    return jsonify(pending), 200


@app.get('/api/companies/accepted')
@user_required(user_type='companies')
def companies_accepted():
    company_id = session.get('email')
    accepted = db_utils.load_students_for_company(company_id, 'accepted')
    return jsonify(accepted), 200


@app.post('/api/companies/cv')
@user_required(user_type='companies')
def companies_cv():
    file, filename = db_utils.load_file(request.json.get('file_id'))
    return send_file(file,
                     as_attachment=True,
                     mimetype='application/pdf',
                     download_name=filename)

# @app.route('/api/companies/cv', methods=['POST'])
# def companies_cv():
#     try:
#         data = request.json
#         file_id = data.get('file_id')
#         if not file_id:
#             return jsonify({'error': 'file_id is required'}), 400
#
#         # 使用 load_file 函数从文件系统中加载文件
#         file_data = db_utils.load_file(file_id)
#         if file_data is None:
#             return jsonify({'error': 'File not found'}), 404
#
#         return send_file(
#             io.BytesIO(file_data.read()),
#             mimetype='application/pdf',
#             as_attachment=True,
#             download_name='cv.pdf'
#         )
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


@app.post('/api/companies/accept')
@user_required(user_type='companies')
def companies_accept():
    company_id = session.get('email')
    # company_id = session.get('email')
    company_query = {'email': company_id}
    company_info = DB.companies.find_one(company_query)
    student_id = request.json.get('student_id')

    student_query = {'email': student_id}
    student_info = DB.students.find_one(student_query)

    if ((student_info is None)
            or (company_info is None)):
            # or (student_id not in company_info['pending'])
            # or (student_id in company_info['accepted'])
            # or (company_id not in student_info['pending'])
            # or (company_id in student_info['accepted'])):
        abort(400)

    DB.students.update_one(student_query, {"$addToSet": {'accepted': company_id}})
    DB.companies.update_one(company_query, {"$addToSet": {'accepted': student_id}})
    DB.students.update_one(student_query, {"$pull": {'pending': company_id}})
    DB.companies.update_one(company_query, {"$pull": {'pending': student_id}})
    return "Succeed", 200


@app.post('/api/companies/reject')
@user_required(user_type='companies')
def companies_refuse():
    company_id = session.get('company_id')
    student_id = request.json.get('student_id')

    DB.students.update_one({'email': student_id}, {"$pull": {'pending': company_id}})
    DB.companies.update_one({'email': company_id}, {"$pull": {'pending': student_id}})

    return jsonify({}), 200


@app.post('/api/companies/cease')
@user_required(user_type='companies')
def companies_cease():
    company_id = session.get('company_id')
    student_id = request.json.get('student_id')

    DB.students.update_one({'email': student_id}, {"$pull": {'accepted': company_id}})
    DB.companies.update_one({'email': company_id}, {"$pull": {'accepted': student_id}})

    return jsonify({}), 200


@app.get('/api/instructors/students')
@user_required(user_type='instructors')
def instructors_students():
    pass


if __name__ == '__main__':
    app.run()
