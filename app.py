from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import bcrypt
import os
from werkzeug.utils import secure_filename
import requests
import string
import bcrypt
from flask_mail import Mail, Message
import random
app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = r'C:\Users\muni karthik\Desktop\blood group\upload'  # Folder where uploaded files will be stored

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
users_collection = db['users']  # This collection contains username, password, and type.
RECAPTCHA_SECRET_KEY = '6LfdhUQqAAAAANuLxNqswzfuSF0PJ7OHk9a2GXii'

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# Route for the login page
@app.route('/', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        username = request.form['Email']
        password = request.form['password'].encode('utf-8')
        entered_code = request.form['captcha_code']

        # Verify if the CAPTCHA code is correct
        if 'captcha_code' in session and session['captcha_code'] != entered_code:
            flash('Invalid code! Please try again.')
            return redirect(url_for('login'))

        # Fetch user from database
        user = users_collection.find_one({'username': username})

        if user:
            if bcrypt.checkpw(password, user['password']):
                session['username'] = username
                session['type'] = user['type']
                if user['type'] == 'hospital':
                    return redirect(url_for('hospital_page'))
                elif user['type'] == 'person':
                    return redirect(url_for('person_page'))
                elif user['type'] == 'police':
                    return redirect(url_for('police_page'))
                else:
                    flash('Invalid user type!')
            else:
                flash('Invalid password!')
        else:
            flash('User not found!')

    # Generate a new CAPTCHA-like code for this session
    session['captcha_code'] = generate_code()

    return render_template('login.html', captcha_code=session['captcha_code'])

# Other routes here...

# Route for the hospital page
@app.route('/hospital')
def hospital_page():
    if 'username' in session and session['type'] == 'hospital':
        return render_template('schedule.html')
    else:
        return redirect(url_for('login'))

# Route for the person page
@app.route('/person')
def person_page():
    if 'username' in session and session['type'] == 'person':
        return "Welcome to the Person's Page!"
    else:
        return redirect(url_for('login'))

# Route for the police page
@app.route('/police')
def police_page():
    if 'username' in session and session['type'] == 'police':
        return "Welcome to the Police's Page!"
    else:
        return redirect(url_for('login'))

# Route for the registration page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# Route to handle registration form submission
@app.route('/register', methods=['POST'])
def register():
    form_data = {
        'first_name': request.form['fname'],
        'last_name': request.form['lname'],
        'gender': request.form['gender'],
        'age': request.form['age'],
        'dob': request.form['dob'],
        'email': request.form['email'],
        'phone': request.form['phone-number'],
        'address': request.form['address'],
        'state': request.form['state'],
        'pincode': request.form['pincode'],
        'aadhar': request.form['aadhar'],
        'blood_group': request.form['Blood_group'],
        'rbc_count': request.form['rbc'],
        'wbc_count': request.form['wbc'],
        'glucose_level': request.form['glucose'],
        'blood_pressure': request.form['bp'],
        'hba1c': request.form['hba1c'],
        'hiv_test': request.form['hiv_test'],
        'other_clinical': request.form['other_clinical']
    }

    # Handle file uploads
    if 'myfile' in request.files:
        photo = request.files['myfile']
        if photo.filename:
            photo_filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            form_data['photo'] = photo_filename

    if 'lab_report' in request.files:
        lab_report = request.files['lab_report']
        if lab_report.filename:
            report_filename = secure_filename(lab_report.filename)
            lab_report.save(os.path.join(app.config['UPLOAD_FOLDER'], report_filename))
            form_data['lab_report'] = report_filename
    
    
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    user_type = request.form['type']
    aadhar_number = request.form['aadhar']
    
    # Check if the username already exists
   
    if users_collection.find_one({'aadhar': aadhar_number}):
        flash('Aadhaar number already exists!')
        return redirect(url_for('register_page'))
    # Hash the password
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Insert user into the database
    users_collection.insert_one({
        'username': username,
        'password': hashed_password,
        'type': user_type,
        'details': form_data  # Store additional user details
    })
    
    flash('Registration successful!')
    return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# from pymongo import MongoClient
# import bcrypt
# import os
# import random
# import string
# from flask_mail import Mail, Message
# from werkzeug.utils import secure_filename

# app = Flask(__name__)
# app.secret_key = 'secret_key'
# app.config['UPLOAD_FOLDER'] = r'C:\Users\muni karthik\Desktop\blood group\upload'

# # MongoDB connection setup
# client = MongoClient('mongodb://localhost:27017/')
# db = client['mydatabase']
# users_collection = db['users']

# # Email config for Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

# mail = Mail(app)

# def generate_code(length=6):
#     return ''.join(random.choices(string.digits, k=length))

# # Route for sending OTP (unchanged)
# @app.route('/send_otp', methods=['POST'])
# def send_otp():
#     email = request.json.get('email')
#     if not email:
#         return jsonify({'status': 'error', 'message': 'Email is required'}), 400

#     otp = generate_code()
#     session['otp'] = otp

#     # Send email
#     try:
#         msg = Message('Your OTP Code', sender='noreply@example.com', recipients=[email])
#         msg.body = f'Your OTP code is {otp}'
#         mail.send(msg)
#         return jsonify({'status': 'success', 'message': 'OTP sent!'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': 'Failed to send OTP'}), 500

# # Route for verifying OTP (unchanged)
# @app.route('/verify_otp', methods=['POST'])
# def verify_otp():
#     entered_otp = request.json.get('otp')
#     if entered_otp == session.get('otp'):
#         return jsonify({'status': 'success', 'message': 'OTP verified!'}), 200
#     return jsonify({'status': 'error', 'message': 'Invalid OTP!'}), 400

# # Registration route (unchanged)
# @app.route('/register', methods=['POST'])
# def register():
#     form_data = {
#         'first_name': request.form['fname'],
#         'last_name': request.form['lname'],
#         'gender': request.form['gender'],
#         'age': request.form['age'],
#         'dob': request.form['dob'],
#         'email': request.form['email'],
#         'phone': request.form['phone-number'],
#         'address': request.form['address'],
#         'state': request.form['state'],
#         'pincode': request.form['pincode'],
#         'aadhar': request.form['aadhar'],
#         'blood_group': request.form['Blood_group'],
#         'rbc_count': request.form['rbc'],
#         'wbc_count': request.form['wbc'],
#         'glucose_level': request.form['glucose'],
#         'blood_pressure': request.form['bp'],
#         'hba1c': request.form['hba1c'],
#         'hiv_test': request.form['hiv_test'],
#         'other_clinical': request.form['other_clinical']
#     }

#     # Handle file uploads (if any)
#     if 'myfile' in request.files:
#         photo = request.files['myfile']
#         if photo.filename:
#             photo_filename = secure_filename(photo.filename)
#             photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
#             form_data['photo'] = photo_filename

#     if 'lab_report' in request.files:
#         lab_report = request.files['lab_report']
#         if lab_report.filename:
#             report_filename = secure_filename(lab_report.filename)
#             lab_report.save(os.path.join(app.config['UPLOAD_FOLDER'], report_filename))
#             form_data['lab_report'] = report_filename
    
#     # Save user details in the database
#     username = request.form['username']
#     password = request.form['password'].encode('utf-8')
#     user_type = request.form['type']
#     aadhar_number = request.form['aadhar']

#     # Check if user exists by Aadhaar number
#     if users_collection.find_one({'aadhar': aadhar_number}):
#         flash('Aadhaar number already exists!')
#         return redirect(url_for('register_page'))

#     # Hash the password
#     hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

#     # Save user to the database
#     users_collection.insert_one({
#         'username': username,
#         'password': hashed_password,
#         'type': user_type,
#         'details': form_data
#     })

#     flash('Registration successful!')
#     return redirect(url_for('login'))

# # New route to render update form with existing details
# @app.route('/search_by_aadhar', methods=['POST'])
# def search_by_aadhar():
#     aadhar = request.form.get('aadhar_search')
#     user = users_collection.find_one({'details.aadhar': aadhar})
    
#     if user:
#         # Convert MongoDB document to a format compatible with Jinja
#         user_data = {
#             'first_name': user['details']['first_name'],
#             'last_name': user['details']['last_name'],
#             'gender': user['details']['gender'],
#             'age': user['details']['age'],
#             'dob': user['details']['dob'],
#             'email': user['details']['email'],
#             'phone': user['details']['phone'],
#             'address': user['details']['address'],
#             'state': user['details']['state'],
#             'pincode': user['details']['pincode'],
#             'aadhar': user['details']['aadhar'],
#             'blood_group': user['details']['blood_group'],
#             'rbc': user['details']['rbc_count'],
#             'wbc': user['details']['wbc_count'],
#             'glucose': user['details']['glucose_level'],
#             'bp': user['details']['blood_pressure'],
#             'hba1c': user['details']['hba1c'],
#             'hiv_test': user['details']['hiv_test'],
#             'other_clinical': user['details']['other_clinical'],
#         }
#         return render_template('update_person.html', user=user_data)
#     else:
#         flash('User not found')
#         return redirect(url_for('update_person_form'))
# @app.route('/update_person/<aadhar>', methods=['POST'])
# def update_person(aadhar):
#     form_data = {
#         'first_name': request.form['fname'],
#         'last_name': request.form['lname'],
#         'gender': request.form['gender'],
#         'age': request.form['age'],
#         'dob': request.form['dob'],
#         'email': request.form['email'],
#         'phone': request.form['phone-number'],
#         'address': request.form['address'],
#         'state': request.form['state'],
#         'pincode': request.form['pincode'],
#         'blood_group': request.form['Blood_group'],
#         'rbc_count': request.form['rbc'],
#         'wbc_count': request.form['wbc'],
#         'glucose_level': request.form['glucose'],
#         'blood_pressure': request.form['bp'],
#         'hba1c': request.form['hba1c'],
#         'hiv_test': request.form['hiv_test'],
#         'other_clinical': request.form['other_clinical']
#     }
#     result = users_collection.update_one(
#         {'details.aadhar': aadhar},
#         {'$set': {'details': form_data}}
#     )
#     if result.matched_count:
#         flash('Details updated successfully!')
#     else:
#         flash('User not found or update failed.')

#     return redirect(url_for('update_person_form'))

# @app.route('/update_person/<aadhar>', methods=['POST'])
# def update_person(aadhar):
#     user = users_collection.find_one({'aadhar': aadhar})
#     if not user:
#         flash('User not found!')
#         return redirect(url_for('some_page'))
    
#     form_data = {
#         'first_name': request.form['fname'],
#         'last_name': request.form['lname'],
#         'gender': request.form['gender'],
#         'age': request.form['age'],
#         'dob': request.form['dob'],
#         'email': request.form['email'],
#         'phone': request.form['phone-number'],
#         'address': request.form['address'],
#         'state': request.form['state'],
#         'pincode': request.form['pincode'],
#         'blood_group': request.form['Blood_group'],
#         'rbc_count': request.form['rbc'],
#         'wbc_count': request.form['wbc'],
#         'glucose_level': request.form['glucose'],
#         'blood_pressure': request.form['bp'],
#         'hba1c': request.form['hba1c'],
#         'hiv_test': request.form['hiv_test'],
#         'other_clinical': request.form['other_clinical']
#     }
#     if 'myfile' in request.files:
#         photo = request.files['myfile']
#         if photo.filename:
#             photo_filename = secure_filename(photo.filename)
#             photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
#             form_data['photo'] = photo_filename

#     if 'lab_report' in request.files:
#         lab_report = request.files['lab_report']
#         if lab_report.filename:
#             report_filename = secure_filename(lab_report.filename)
#             lab_report.save(os.path.join(app.config['UPLOAD_FOLDER'], report_filename))
#             form_data['lab_report'] = report_filename

#     # Update the user's details in the database
#     users_collection.update_one({'aadhar': aadhar}, {'$set': {'details': form_data}})
    
#     flash('Details updated successfully!')
#     return redirect(url_for('some_page'))

# if __name__ == '__main__':
#     if not os.path.exists(app.config['UPLOAD_FOLDER']):
#         os.makedirs(app.config['UPLOAD_FOLDER'])
#     app.run(debug=True)
