import math

import cloudinary.uploader
from flask import render_template, request, redirect
from flask_login import login_user, logout_user

from qlhs import app, dao, login
from qlhs.decorators import anonymous_user
from qlhs.admin import *

@app.route('/')
def index():
    students = dao.load_students(class_id=request.args.get('class_id'),
                                 kw=request.args.get('keyword'),
                                 page=int(request.args.get('page', 1)))
    counter = dao.count_students()

    return render_template('index.html',
                           students=students,
                           pages=math.ceil(counter / app.config['PAGE_SIZE']))


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password,
                             avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
@anonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            return redirect('/')

    return render_template('login.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/students/<int:student_id>')
def details(student_id):
    s = dao.get_student_by_id(student_id)
    return render_template('details.html', student=s)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_attributes():
    classes = dao.load_classes()
    return {
        'classes': classes
    }


@app.route('/scores_details/<int:student_id>', methods=['post', 'get'])
def scores_details(student_id):
    stud = dao.get_student_by_id(student_id=student_id)
    sem = dao.load_semester()
    sub = dao.load_subjects()
    year = dao.load_school_year()
    subject_id = request.form.get('subject_name')
    semester_id = request.form.get('semester_name')
    year_id = request.form.get('year_name')
    s = dao.get_subject_by_id(subject_id=subject_id)
    se = dao.get_semester_by_id(semester_id=semester_id)
    ye = dao.get_year_by_id(year_id=year_id)
    scores = dao.load_scores(student_id=student_id,
                             subject_id=subject_id,
                             semester_id=semester_id,
                             year_id=year_id)
    avg_scores = dao.load_avg_scores(student_id=student_id,
                                     subject_id=subject_id,
                                     semester_id=semester_id,
                                     year_id=year_id)

    return render_template('scores.html', sem=sem,
                           sub=sub, year=year, stud=stud, scores=scores,
                           avg_scores=avg_scores, s=s, se=se, ye=ye)


@app.route('/avg', methods=['get', 'post'])
def avg():
    classes = dao.load_classes()
    class_id = request.form.get('class_name')
    students = dao.load_students(class_id=class_id)
    student_id = request.form.get('student_name')
    semesters = dao.load_semester()
    semester_id = request.form.get('semester_name')
    years = dao.load_school_year()
    year_id = request.form.get('year_name')
    s = dao.get_student_by_id(student_id=student_id)
    se = dao.get_semester_by_id(semester_id=semester_id)
    ye = dao.get_year_by_id(year_id=year_id)
    avg_scores = dao.load_avg_sem(student_id=student_id, semester_id=semester_id, year_id=year_id)
    return render_template('avg.html', classes=classes, students=students, semesters=semesters, years=years,
                           avg_scores=avg_scores, class_id=class_id, s=s, se=se, ye=ye)


if __name__ == '__main__':
    app.run(debug=True)
