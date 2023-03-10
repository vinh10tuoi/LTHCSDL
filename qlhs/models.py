from enum import Enum as UserEnum

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Enum, Float
from sqlalchemy.orm import relationship, backref

from qlhs import db, app


class UserRole(UserEnum):
    user = 1
    admin = 2


class UserGender(UserEnum):
    male = 1
    female = 2


class UserSemester(UserEnum):
    HKI = 1
    HKII = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Class(BaseModel):
    name = Column(String(50), nullable=False)
    total_students = Column(Integer, nullable=False)
    students = relationship('Student', backref='class', lazy=True)
    details = relationship('ScoreDetails', backref='class', lazy=True)

    def __str__(self):
        return self.name


stud_subject = db.Table('stud_subject',
                        Column('student_id', ForeignKey('student.id'), nullable=False, primary_key=True),
                        Column('subject_name', ForeignKey('subject.id'), nullable=False, primary_key=True))

seme_subject = db.Table('seme_subject',
                        Column('seme_id', ForeignKey('semester.id'), nullable=False, primary_key=True),
                        Column('subject_name', ForeignKey('subject.id'), nullable=False, primary_key=True))


class Student(BaseModel):
    name = Column(String(50), nullable=False)
    birthday = Column(Date, nullable=False)
    phone_number = Column(String(50))
    gender = Column(Enum(UserGender), nullable=False)
    image = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    email = Column(String(100))
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    subjects = relationship('Subject', secondary='stud_subject', lazy='subquery',
                            backref=backref('students', lazy=True))
    details = relationship('ScoreDetails', backref='student', lazy=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.user)

    def __str__(self):
        return self.name


class Subject(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    semesters = relationship('Semester', secondary='seme_subject', lazy='subquery',
                             backref=backref('subjects', lazy=True))
    details = relationship('ScoreDetails', backref='subject', lazy=True)

    def __str__(self):
        return self.name


class ScoreType(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    details = relationship('ScoreDetails', backref='score', lazy=True)

    def __str__(self):
        return self.name


class Semester(BaseModel):
    name = Column(Enum(UserSemester), nullable=False)
    details = relationship('ScoreDetails', backref='semester', lazy=True)


class SchoolYear(BaseModel):
    name = Column(String(50), nullable=False)
    details = relationship('ScoreDetails', backref='year', lazy=True)

    def __str__(self):
        return self.name


class ScoreDetails(BaseModel):
    value = Column(Float, nullable=False)
    score_id = Column(Integer, ForeignKey(ScoreType.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    year_id = Column(Integer, ForeignKey(SchoolYear.id), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    __table_args__ = (
                         db.CheckConstraint('value >= 0 and value <= 10', name='check_value')
                     ),


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
        import hashlib

        password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())

        u = User(name='Tuyen', username='admin', password=password,
                 avatar='https://res.cloudinary.com/dzbcst18v/image/upload/v1670219693/boy_rcrqid.png',
                 user_role=UserRole.admin)

        db.session.add(u)
        db.session.commit()

        c1 = Class(name='10A1', total_students=3)
        c2 = Class(name='11A1', total_students=3)
        c3 = Class(name='12A1', total_students=3)
        db.session.add_all([c1, c2, c3])
        db.session.commit()

        s1 = Student(name='?????ng Ph?????c Tuy???n', birthday='2001/01/01',
                     phone_number='0932012306', gender=UserGender.male,
                     image='https://res.cloudinary.com/dzbcst18v/image/upload/v1670219693/boy_rcrqid.png',
                     address='157/20 Ph???m V??n Chi??u, ph?????ng 14, qu???n G?? V???p',
                     email='dptuyen1@gmail.com', class_id=1)
        s2 = Student(name='Nguy???n Tr???ng Nh??n', birthday='2001/12/19',
                     phone_number='0936665674', gender=UserGender.male,
                     image='https://res.cloudinary.com/dzbcst18v/image/upload/v1670219693/boy_rcrqid.png',
                     address='82/2 ???????ng s??? 14, ph?????ng 08, qu???n G?? V???p',
                     email='ntnhan@gmail.com', class_id=2)
        s3 = Student(name='Nguy???n Thanh To??n', birthday='2001/05/19',
                     phone_number='0777618759', gender=UserGender.male,
                     image='https://res.cloudinary.com/dzbcst18v/image/upload/v1670219693/boy_rcrqid.png',
                     address='Th???ng Nh???t, ph?????ng 10, qu???n G?? V???p',
                     email='nttoan@gmail.com', class_id=3)

        db.session.add_all([s1, s2, s3])
        db.session.commit()
        #
        # sem1 = Semester(name=UserSemester.HKI)
        # sem2 = Semester(name=UserSemester.HKII)
        # db.session.add_all([sem1, sem2])
        # db.session.commit()
        #
        # st1 = ScoreType(name='15 ph??t')
        # st2 = ScoreType(name='1 ti???t')
        # st3 = ScoreType(name='Gi???a k???')
        # st4 = ScoreType(name='Cu???i k???')
        # db.session.add_all([st1, st2, st3, st4])
        # db.session.commit()
        #
        # y = SchoolYear(name='2022-2023')
        # db.session.add(y)
        # db.session.commit()
        #
        # sub1 = Subject(name='To??n')
        # sub2 = Subject(name='Ti???ng Anh')
        # db.session.add_all([sub1, sub2])
        # db.session.commit()

        # s4 = Student(name='Tr???n H???u Ph?????c Th??nh', birthday='2001/02/27',
        #              phone_number='0909116007', gender=UserGender.male,
        #              image='https://res.cloudinary.com/dzbcst18v/image/upload/v1670219693/boy_rcrqid.png',
        #              address='688 Quang Trung, ph?????ng 11, qu???n G?? V???p',
        #              email='thpthanh@gmail.com', class_id=1)
        # s5 = Student(name='Nguy???n Ph???ng Nghi', birthday='2001/10/19',
        #              phone_number='0899304255', gender=UserGender.female,
        #              image='https://res.cloudinary.com/dzbcst18v/image/upload/v1670219693/girl_fqrhhe.png',
        #              address='14/8A ???????ng s??? 30, ph?????ng 06, qu???n G?? V???p',
        #              email='npnghi1910@gmail.com', class_id=2)
        # s6 = Student(name='Tr???n L?? Th??y Vi', birthday='2001/03/26',
        #              phone_number='0937934910', gender=UserGender.female,
        #              image='https://res.cloudinary.com/dzbcst18v/image/upload/v1670219693/girl_fqrhhe.png',
        #              address='234 L?? ?????c Th???. ph?????ng 06, qu???n G?? V???p',
        #              email='tltvi@gmail.com', class_id=3)
        # s7 = Student(name='Nguy???n V??n Th???ng', birthday='2001/05/16',
        #              phone_number='0901105751', gender=UserGender.male,
        #              image='https://res.cloudinary.com/dzbcst18v/image/upload/v1670219693/boy_rcrqid.png',
        #              address='Nguy???n V??n Qu??, ph?????ng ????ng H??ng Thu???n, qu???n 12',
        #              email='nvthong@gmail.com', class_id=1)
        # s8 = Student(name='Hu???nh Anh Khoa', birthday='2001/08/23',
        #              phone_number='0976178235', gender=UserGender.male,
        #              image='https://res.cloudinary.com/dzbcst18v/image/upload/v1670219693/boy_rcrqid.png',
        #              address='Th???ng Nh???t, ph?????ng 16, qu???n G?? V???p',
        #              email='hakhoa@gmail.com', class_id=2)
        # s9 = Student(name='Chu Ho??ng D??? Ch??u', birthday='2000/11/21',
        #              phone_number='0707214934', gender=UserGender.female,
        #              image='https://res.cloudinary.com/dzbcst18v/image/upload/v1670219693/girl_fqrhhe.png',
        #              address='???????ng s??? 59, ph?????ng 14, qu???n G?? V???p',
        #              email='chdchau@gmail.com', class_id=3)
        # db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9])
        # db.session.commit()
