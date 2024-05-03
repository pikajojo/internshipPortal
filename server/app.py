import os
import requests
import tempfile
from dotenv import load_dotenv
from flask import Flask, Response, request, jsonify, session, abort, redirect
from flask_session import Session
from auth import verify_token, login_required, user_required
from config import MONGODB_CLIENT, DB
import db_utils

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.config['SESSION_TYPE'] = "mongodb"
app.config['SESSION_MONGODB'] = MONGODB_CLIENT
app.config['SESSION_MONGODB_DB'] = os.getenv("MONGODB_DB")
app.config['SESSION_MONGODB_COLLECTION'] = os.getenv("SESSION_MONGODB_COLLECTION")
Session(app)


@app.get('/api/whoami')
def whoami():
    if session.get('google_id') is not None:
        return jsonify(db_utils.load_user_info(session.get('user_type'), session.get('google_id'))), 200
    return jsonify({}), 200


@app.post('/api/login')
def login():
    info, e = verify_token(request.json.get('token'))
    if info is None:
        return e, abort(400)
    user = DB.users.find_one({'google_id': info['email']})
    if user is None:
        return "Unknown User", abort(401)
    # "type" field of users collection should always be plural
    # in order to be consistent with the collection name of each
    # user type in the database so that it can be directly used
    # for indexing a collection
    user_info = db_utils.load_user_info(user['user_type'], user['google_id'])
    session['google_id'] = user['google_id']
    session['user_type'] = user['user_type']
    return jsonify(user_info), 200


@app.post('/api/logout')
def logout():
    session.pop('google_id')
    session.pop('user_type')
    return jsonify({}), 200


@app.post('/api/students/edit')
@user_required(user_type='students')
def students_edit():
    student_id = session.get('google_id')
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the file to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        with open(temp_file.name, 'rb') as f:
            content = f.read()

        db_utils.update_cv(student_id, content, file.filename)
        os.unlink(temp_file.name)

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.get('/api/students/companies')
@user_required(user_type='students')
def students_companies():
    companies = db_utils.load_companies_for_student(session.get('google_id'))
    return jsonify(companies), 200


@app.get('/api/students/instructors')
@user_required(user_type='students')
def students_instructors():
    instructors = db_utils.load_instructors_for_student(session.get('google_id'))
    return jsonify(instructors), 200


@app.post('/api/students/apply')
@user_required(user_type='students')
def students_apply():
    student_id = session.get('google_id')
    student_query = {'google_id': student_id}
    student_info = DB.students.find_one(student_query)
    if student_info['cv'] is None:
        return "No CV found", 400
    company_id = request.json.get('company_id')
    company_query = {'google_id': company_id}
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
    company_id = session.get('google_id')
    pending = db_utils.load_students_for_company(company_id, 'pending')
    return jsonify(pending), 200


@app.get('/api/companies/accepted')
@user_required(user_type='companies')
def companies_accepted():
    company_id = session.get('google_id')
    accepted = db_utils.load_students_for_company(company_id, 'accepted')
    return jsonify(accepted), 200


@app.post('/api/companies/cv')
@user_required(user_type='companies')
def companies_cv():
    file = db_utils.load_file(request.json.get('file_id'))
    return Response(file, content_type='application/pdf')


@app.post('/api/companies/accept')
@user_required(user_type='companies')
def companies_accept():
    company_id = session.get('company_id')
    company_query = {'google_id': company_id}
    company_info = DB.companies.find_one(company_query)
    student_id = request.json.get('student_id')
    student_query = {'google_id': student_id}
    student_info = DB.students.find_one(student_query)

    if ((student_info is None)
            or (company_info is None)
            or (student_id not in company_info['pending'])
            or (student_id in company_info['accepted'])
            or (company_id not in student_info['pending'])
            or (company_id in student_info['accepted'])):
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

    DB.students.update_one({'google_id': student_id}, {"$pull": {'pending': company_id}})
    DB.companies.update_one({'google_id': company_id}, {"$pull": {'pending': student_id}})

    return jsonify({}), 200


@app.post('/api/companies/cease')
@user_required(user_type='companies')
def companies_cease():
    company_id = session.get('company_id')
    student_id = request.json.get('student_id')

    DB.students.update_one({'google_id': student_id}, {"$pull": {'accepted': company_id}})
    DB.companies.update_one({'google_id': company_id}, {"$pull": {'accepted': student_id}})

    return jsonify({}), 200


@app.get('/api/instructors/students')
@user_required(user_type='instructors')
def instructors_students():
    pass


if __name__ == '__main__':
    app.run()
