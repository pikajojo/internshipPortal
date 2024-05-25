
import os
import requests
import tempfile

import werkzeug
from bson import json_util
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
            data['pending'] = []
            data['accepted'] = []
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

    if company_info is None:
        return jsonify({'error': 'Invalid company data'}), 400
    if 'pending' not in company_info:
        company_info['pending'] = []
        DB.companies.update_one(company_query, {"$set": {'pending': company_info['pending']}})
    if 'accepted' not in company_info:
        company_info['accepted'] = []
        DB.companies.update_one(company_query, {"$set": {'accepted': company_info['accepted']}})

    if (student_id in company_info['pending']) or (student_id in company_info['accepted']):
        return jsonify({'error': 'Already applied'}), 400

    DB.students.update_one(student_query, {"$addToSet": {'pending': company_id}})
    DB.companies.update_one(company_query, {"$addToSet": {'pending': student_id}})

    return jsonify({'success': 'Application successful'}), 200


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

@app.post('/api/instructors/cv')
@user_required(user_type='instructors')
def instructors_cv():
    file, filename = db_utils.load_file(request.json.get('file_id'))
    return send_file(file,
                     as_attachment=True,
                     mimetype='application/pdf',
                     download_name=filename)

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

@app.get('/api/instructors/toreview')
@user_required(user_type='instructors')
def instructors_to_review():
    instructor_id = session.get('email')
    to_review_students = db_utils.load_to_review_students_for_instructor(instructor_id)
    return jsonify(to_review_students), 200
@app.get('/api/instructors/reviewed')
@user_required(user_type='instructors')
def instructors_reviewed():
    instructor_id = session.get('email')
    reviewed_students = db_utils.load_reviewed_students_for_instructor(instructor_id)
    return jsonify(reviewed_students), 200

@app.post('/api/instructors/message')
@user_required(user_type='instructors')
def instructors_send_message():
    data = request.json
    student_id = data.get('student_id')
    message = data.get('message')

    if not student_id or not message:
        return jsonify({'error': 'student_id and message are required'}), 400

    result = db_utils.send_message_to_student(session['email'], student_id, message)

    if result:
        return jsonify({'message': 'Message sent successfully'}), 200
    else:
        return jsonify({'error': 'Failed to send message'}), 500

@app.post('/api/instructors/review')
@user_required(user_type='instructors')
def instructors_review():
    data = request.json
    student_id = data.get('student_id')

    if not student_id:
        return jsonify({'error': 'student_id is required'}), 400

    result = db_utils.review_student(session['email'], student_id)

    if result:
        return jsonify({'message': 'Student reviewed successfully'}), 200
    else:
        return jsonify({'error': 'Failed to review student'}), 500

@app.post('/api/students/message')
@user_required(user_type='students')
def students_send_message():
    student_id = session.get('email')
    company_id = request.json.get('company_id')
    message = request.json.get('message').strip()
    # student_info = DB.students.find_one({'email': student_id})

    if not company_id or not message:
        return jsonify({'error': 'Invalid input'}), 400

    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    message_data = {
        'student_id': student_id,
        'company_email': company_id,
        'message': message
    }

    result = DB.messages.insert_one(message_data)

    if result.inserted_id:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': 'Failed to send message'}), 500


@app.get('/api/companies/messages')
@user_required(user_type='companies')
def companies_get_messages():
    try:
        company_id = session.get('email')
        if not company_id:
            return jsonify({"error": "Unauthorized"}), 401

        messages_cursor = DB.messages.find({'company_email': company_id})
        messages = [{message.get('student_Id'), message.get('message')} for message in messages_cursor]
        return json_util.dumps(messages), 200
    except Exception as e:
        # Optionally, you could log the error here if logging is set up
        return jsonify({"error": "Internal Server Error"}), 500


@app.post('/api/companies/message')
@user_required(user_type='companies')
def companies_send_message():
    company_id = session.get('email')
    student_id = request.json.get('student_id')
    message = request.json.get('message')
    company_info = DB.companies.find_one({'email': company_id})

    if not company_info or not student_id or not message:
        return jsonify({'error': 'Invalid input'}), 400

    message_data = {
        'company_email': company_id,
        'company_name': company_info['name'],
        'student_email': student_id,
        'message': message
    }

    result = DB.messages.insert_one(message_data)

    if result.inserted_id:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': 'Failed to send message'}), 500


@app.get('/api/students/messages')
@user_required(user_type='students')
def students_get_messages():
    try:
        student_id = session.get('email')
        if not student_id:
            return jsonify({"error": "Unauthorized"}), 401

        # 从数据库中查询消息，假设 DB 是您的数据库连接对象
        messages_cursor = DB.messages.find({'student_email': student_id})

        # 将游标转换为列表，并确保每个消息都是一个标准的 Python 字典
        messages = [message for message in messages_cursor]

        # 日志记录查询到的消息，用于调试
        # app.logger.debug(f"Fetched messages for student {student_id}: {messages}")

        # 返回 JSON 响应
        return json_util.dumps(messages), 200
    except Exception as e:
        # app.logger.error(f"Error fetching messages: {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    app.run()