from flask import Flask, render_template, request
from model import retrieve_csv_data, majors_at_fisk, is_all_empty, is_valid_password
from flask import render_template
from flask import request, redirect, session, url_for, session
from flask_pymongo import PyMongo
import secrets
import bcrypt


app = Flask(__name__)

@app.route('/')
@app.route('/upload', methods=['GET', 'POST'])
def index():
    return render_template('upload.html')

# @app.route('/')
# @app.route('/login', methods=['GET', 'POST'])



# @app.route('/studentSignup', methods=['GET', 'POST'])
# def student_signup():
#     if request.method == "POST":
#         student_users = mongo.db.users_info
#         #search for username in database
#         student_id = request.form['id']
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         middle_name = request.form['middle_name']
#         student_email = request.form['student_email']
#         password_unencrypted = request.form['password']
#         password_unencrypted1 = request.form['password1'] #confirm your password section

#         if password_unencrypted != password_unencrypted1:
#             return render_template("studentSignup.html")

#         #checks if both password and username format is empty
#         if is_all_empty(student_id) and is_all_empty(password_unencrypted):
#             return render_template("signup.html")
#         #checks if username format is empty
#         elif is_all_empty(student_id):
#             return render_template("studentSignup.html")
#         #checks if the password is empty
#         elif is_all_empty(password_unencrypted):
#             return render_template("studentSignup.html")
#         #checks if the password is valid or not
#         elif not is_valid_password(password_unencrypted):
#             return render_template("studentSignup.html")
        
#         existing_user = student_users.find_one({'student_email':student_email})

#         #if user not in database
#         if not existing_user:
#             #encode password for hashing
#             password = (request.form['password']).encode("utf-8")        
#             #hash password
#             salt = bcrypt.gensalt()
#             hashed = bcrypt.hashpw(password, salt)
#             #add new user to database
#             student_users.insert_one({'name': {'first_name': first_name, 'last_name':last_name, 'middle_name': middle_name, 'student_id': student_id}, 'password': hashed, 'student_email':student_email})
#             #store username in session
#             return render_template('login.html')
#         else:
#             return 'Username already registered.Try logging in.'  
#     else:
#         return render_template('studentSignup.html')

# @app.route('/')
# @app.route('/FacultySignup', methods=['GET', 'POST'])
# def faculty_signup():
#     if request.method == "POST":
#         student_users = mongo.db.users_info
#         #search for username in database
#         student_id = request.form['id']
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         middle_name = request.form['middle_name']
#         student_email = request.form['student_email']
#         password_unencrypted = request.form['password']
#         password_unencrypted1 = request.form['password1'] #confirm your password section

#         if password_unencrypted != password_unencrypted1:
#             return render_template("studentSignup.html")

#         #checks if both password and username format is empty
#         if is_all_empty(student_id) and is_all_empty(password_unencrypted):
#             return render_template("signup.html")
#         #checks if username format is empty
#         elif is_all_empty(student_id):
#             return render_template("studentSignup.html")
#         #checks if the password is empty
#         elif is_all_empty(password_unencrypted):
#             return render_template("studentSignup.html")
#         #checks if the password is valid or not
#         elif not is_valid_password(password_unencrypted):
#             return render_template("studentSignup.html")
        
#         existing_user = student_users.find_one({'student_email':student_email})

#         #if user not in database
#         if not existing_user:
#             #encode password for hashing
#             password = (request.form['password']).encode("utf-8")        
#             #hash password
#             salt = bcrypt.gensalt()
#             hashed = bcrypt.hashpw(password, salt)
#             #add new user to database
#             student_users.insert_one({'name': {'first_name': first_name, 'last_name':last_name, 'middle_name': middle_name, 'student_id': student_id}, 'password': hashed, 'student_email':student_email})
#             #store username in session
#             return render_template('login.html')
#         else:
#             return 'Username already registered.Try logging in.'  
#     else:
#         return render_template('facultySignup.html')


@app.route('/broucherList')
@app.route('/broucherList', methods=['GET', 'POST'])
def graduation_broucher():
    if request.method == "POST":
        csv_file = request.form['filename']
        if csv_file[-3:] != 'csv':
            return render_template('redirect.html')
        data = retrieve_csv_data(csv_file)
        return render_template('broucherList.html', student_data = data, majors = majors_at_fisk(csv_file))
    return render_template('broucherList.html')

if __name__ == "__main__":
    app.run()