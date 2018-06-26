from django.conf.urls import url
from ertaapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.CourseListView.as_view(), name='course_list'),
    url(r'^course/(?P<pk>\d+)$', views.ContentListView.as_view(), name='content_list'),
    url(r'^content/(?P<pk>\d+)/(?P<pk_alt>\d+)$', views.ContentDetailView.as_view(), name='content_detail'),
    url(r'^teacher_courses/$', views.AdmincourseListView.as_view(), name='teacher_course_list'),
    url(r'^course_messages/(?P<pk>\d+)$', views.MessagecourseListView.as_view(), name='message_course_list'),
    url(r'^students/(?P<pk>\d+)$', views.StudentsListView.as_view(), name='students_list'),
    url(r'^students/content/(?P<pk>\d+)/(?P<pk_alt>\d+)$', views.ScontentListView.as_view(), name='student_content'),
    url(r'^student_answers$', views.StudentanswerListView.as_view(), name='student_answers'),
    url(r'^student_messages$', views.StudentmessageListView.as_view(), name='student_messages'),
    url(r'^send_message$', views.SendMessageView.as_view(), name='send_message'),
    url(r'^add_student$', views.AddStudentView.as_view(), name='add_student'),
    url(r'^add_course$', views.AddCourseView.as_view(), name='add_course'),
    url(r'^add_content$', views.AddContentView.as_view(), name='add_content'),
    url(r'^student/score/(?P<pk>\d+)/(?P<pk_alt>\d+)$', views.SetScoreView.as_view(), name='set_student_score'),
    url(r'^student/score/(?P<pk>\d+)/(?P<pk_alt>\d+)/edit$', views.ScoreUpdateView.as_view(), name='change_student_score'),
    url(r'^course/answers/(?P<pk>\d+)$', views.CourseAnswersListView.as_view(), name='course_answers'),
    url(r'^content/add_answer/(?P<pk>\d+)/(?P<pk_alt>\d+)$', views.AddAnswerView.as_view(), name='add_answer'),
    url(r'^content/(?P<pk>\d+)/(?P<pk_alt>\d+)/edit$', views.ContentUpdateView.as_view(), name='update_content'),
    url(r'^reply_message/(?P<pk>\d+)/(?P<pk_alt>\d+)$', views.ReplyMessageView.as_view(), name='reply_to_message'),
    url(r'^teacher_messages/$', views.TeacherMessagesView.as_view(), name='teacher_messages'),
    url(r'^student_answers_all/$', views.StudentsAnswersView.as_view(), name='student_answers_all'),
    url(r"login/$", auth_views.LoginView.as_view(template_name="ertaapp/login.html"),name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUp.as_view(), name="signup"),
    url(r'^course/(?P<pk>\d+)/edit$', views.CourseUpdateView.as_view(), name='edit_course'),
    url(r'^course/(?P<pk>\d+)/remove$', views.CourseDeleteView.as_view(), name='course_remove'),
    url(r'^content/(?P<pk>\d+)/remove$', views.ContentDeleteView.as_view(), name='content_remove'),
]
