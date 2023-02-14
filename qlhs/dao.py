import hashlib

from qlhs import app, db
from qlhs.models import Class, Student, User, Semester, Subject, ScoreDetails, SchoolYear


def load_classes():
    return Class.query.all()


def load_students(class_id=None, kw=None, page=1):
    query = Student.query.filter()

    if class_id:
        query = query.filter(Student.class_id.__eq__(class_id))

    if kw:
        query = query.filter(Student.name.contains(kw))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return query.slice(start, end).all()


def load_semester():
    return Semester.query.all()


def load_subjects():
    return Subject.query.all()


def load_school_year():
    return SchoolYear.query.all()


def count_students():
    return Student.query.filter().count()


def get_student_by_id(student_id):
    return Student.query.get(student_id)


def get_class_by_id(class_id):
    return Class.query.get(class_id)


def get_subject_by_id(subject_id):
    return Subject.query.get(subject_id)


def get_semester_by_id(semester_id):
    return Semester.query.get(semester_id)


def get_year_by_id(year_id):
    return SchoolYear.query.get(year_id)


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_scores(student_id, subject_id, semester_id, year_id):
    query = ScoreDetails.query.filter(ScoreDetails.student_id.__eq__(student_id),
                                      ScoreDetails.subject_id.__eq__(subject_id),
                                      ScoreDetails.semester_id.__eq__(semester_id),
                                      ScoreDetails.year_id.__eq__(year_id)).order_by(ScoreDetails.score_id)

    return query.all()


def load_avg_scores(student_id, subject_id, semester_id, year_id):
    scores_list = ScoreDetails.query.filter(ScoreDetails.student_id.__eq__(student_id),
                                            ScoreDetails.subject_id.__eq__(subject_id),
                                            ScoreDetails.semester_id.__eq__(semester_id),
                                            ScoreDetails.year_id.__eq__(year_id)).all()
    total_scores = ScoreDetails.query.filter(ScoreDetails.student_id.__eq__(student_id),
                                             ScoreDetails.subject_id.__eq__(subject_id),
                                             ScoreDetails.semester_id.__eq__(semester_id),
                                             ScoreDetails.year_id.__eq__(year_id)).count()
    sum_sc = 0
    for i in scores_list:
        sum_sc += float(i.value)
    if total_scores >= 1:
        avg_sc = sum_sc / total_scores
    else:
        avg_sc = 0
    return avg_sc


def load_avg_sem(student_id, semester_id, year_id):
    scores_list = ScoreDetails.query.filter(ScoreDetails.student_id.__eq__(student_id),
                                            ScoreDetails.semester_id.__eq__(semester_id),
                                            ScoreDetails.year_id.__eq__(year_id)).all()
    total_scores = ScoreDetails.query.filter(ScoreDetails.student_id.__eq__(student_id),
                                             ScoreDetails.semester_id.__eq__(semester_id),
                                             ScoreDetails.year_id.__eq__(year_id)).count()
    sum_sc = 0
    for i in scores_list:
        sum_sc += float(i.value)
    if total_scores >= 1:
        avg_sc = sum_sc / total_scores
    else:
        avg_sc = 0
    return avg_sc
