from flask import redirect
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from qlhs import app, db
from qlhs.models import Class, Student, UserRole, Subject, ScoreType, Semester, ScoreDetails, SchoolYear

admin = Admin(app=app, name='TVC High-school Administration',
              template_mode='bootstrap4')


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated \
               and current_user.user_role == UserRole.admin


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class StudentView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'birthday']
    column_filters = ['name', 'gender']
    column_exclude_list = ['image']
    column_labels = {
        'name': 'Tên',
        'birthday': 'Ngày sinh',
        'phone_number': 'Số điện thoại',
        'gender': 'Giới tính',
        'address': 'Địa chỉ',
        'class': 'Lớp'
    }
    page_size = 4
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']


class SubjectView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']


class ScoreView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True


class SemesterView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True


class ScoreDetailsView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_filters = ['value', 'student.name']


class SchoolYearView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(AuthenticatedModelView(Class, db.session, name='Lớp'))
admin.add_view(StudentView(Student, db.session, name='Học sinh'))
admin.add_view(SubjectView(Subject, db.session, name='Môn học'))
admin.add_view(ScoreDetailsView(ScoreDetails, db.session, name='Bảng điểm'))
admin.add_view(ScoreView(ScoreType, db.session, name='Loại điểm'))
admin.add_view(SemesterView(Semester, db.session, name='Học kỳ'))
admin.add_view(SchoolYearView(SchoolYear, db.session, name='Năm học'))
admin.add_view(StatsView(name='Thống kế - Báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
