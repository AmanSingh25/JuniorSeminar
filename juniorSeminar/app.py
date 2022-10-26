import os
from flask import Flask, render_template, request
from model import retrieve_csv_data, majors_at_fisk, is_all_empty, is_valid_password
from flask import render_template
import pymongo
from flask import request, redirect, session, url_for, session
from flask_pymongo import PyMongo
import secrets
import bcrypt


app = Flask(__name__)


client = pymongo.MongoClient("mongodb+srv://admin1:bns5Fzi1oQSglRmJ@cluster0.zvj7jes.mongodb.net/?retryWrites=true&w=majority")
db = client.database

#session data
app.secret_key = secrets.token_urlsafe(16)

# @app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# @app.route('/')
# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     return render_template('upload.html')

# @app.route('/')
# @app.route('/login', methods=['GET', 'POST'])


@app.route('/studentSignup', methods=['GET', 'POST'])
def student_signup():
    if request.method == "POST":
        student_users = db.student_info
        #search for username in database
        student_id = request.form['id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        student_email = request.form['student_email']
        password_unencrypted = request.form['password']
        password_unencrypted1 = request.form['password1'] #confirm your password section

        if password_unencrypted != password_unencrypted1:
            return render_template("studentSignup.html")

        #checks if both password and username format is empty
        if is_all_empty(student_id) and is_all_empty(password_unencrypted):
            return render_template("studentSignup.html")
        #checks if username format is empty
        elif is_all_empty(student_id):
            return render_template("studentSignup.html")
        #checks if the password is valid or not
        elif not is_valid_password(password_unencrypted):
            return render_template("studentSignup.html")
        
        existing_user = student_users.find_one({'student_email':student_email})

        #if user not in database
        if not existing_user:
            #encode password for hashing
            password = (request.form['password']).encode("utf-8")        
            #hash password
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password, salt)
            #add new user to database
            student_users.insert_one({'name': {'first_name': first_name, 'last_name':last_name, 'middle_name': middle_name, 'student_id': student_id}, 'password': hashed, 'student_email':student_email})
            #store username in session
            return render_template('studentSignin.html')
        else:
            return 'Username already registered.Try logging in.'  
    else:
        return render_template('studentSignup.html')

@app.route('/')
@app.route('/studentSignin', methods=['GET', 'POST'])
def student_signin():
    if request.method == "POST":
        users = db.student_info
        #search for username in database
        login_user = users.find_one({'student_email': request.form['useremail']})

        #if username in database
        if login_user:
            db_password = login_user['password']
                #store username and user's image in session
            session['useremail'] = request.form['useremail']
            #encode password
            password = request.form['password'].encode("utf-8")
            #compare username in database to username submitted in form
            if bcrypt.checkpw(password, db_password):
                return "Access provided"
            else:
                return 'Invalid username/password combination.'
        else:
            return 'User not found. Please try Signing in'
    else:
        return render_template('studentSignin.html')


# @app.route('/')
@app.route('/facultySignup', methods=['GET', 'POST'])
def faculty_signup():
    if request.method == "POST":
        faculty_users = db.faculty_info
        #search for username in database
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        faculty_email = request.form['faculty_email']
        faculty_discipline = request.form['discipline']
        password_unencrypted = request.form['password']
        password_unencrypted1 = request.form['password1'] #confirm your password section

        if password_unencrypted != password_unencrypted1:
            return render_template("facultySignup.html")

        #checks if both password and username format is empty
        if is_all_empty(faculty_email) and is_all_empty(password_unencrypted):
            return render_template("facultySignup.html")
        # #checks if the password is valid or not
        elif not is_valid_password(password_unencrypted):
            return render_template("facultySignup.html")
        
        existing_user = faculty_users.find_one({'faculty_email':faculty_email})

        #if user not in database
        if not existing_user:
            #encode password for hashing
            password = (request.form['password']).encode("utf-8")        
            #hash password
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password, salt)
            #add new user to database
            faculty_users.insert_one({'name': {'first_name': first_name, 'last_name':last_name, 'middle_name': middle_name}, 'password': hashed, 'faculty_email':faculty_email, 'faculty_discipline':faculty_discipline})
            #store username in session
            return render_template("facultySignin.html")
        else:
            return 'Username already registered.Try logging in.'
    else:  
        return render_template("facultySignup.html")

# @app.route('/')
@app.route('/facultySignin', methods=['GET', 'POST'])
def faculty_signin():
    if request.method == "POST":
        users = db.faculty_info
        #search for username in database
        login_user = users.find_one({'faculty_email': request.form['useremail']})

        #if username in database
        if login_user:
            db_password = login_user['password']
                #store username and user's image in session
            session['useremail'] = request.form['useremail']
            #encode password
            password = request.form['password'].encode("utf-8")
            #compare username in database to username submitted in form
            if bcrypt.checkpw(password, db_password):
                return render_template("upload.html")
            else:
                return 'Invalid username/password combination.'
        else:
            return 'User not found. Please try Signing in'
    else:
        return render_template('facultySignin.html')

# @app.route('/studentSignin', methods=['GET', 'POST'])
# def student_signin():
#     return render_template('studentSignin.html')

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
