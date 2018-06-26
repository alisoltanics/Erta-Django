from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db import connection
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from ertaapp.forms import CourseForm, CourseMemberForm, ReplyMessageForm, MessageForm, ContentForm, ScoreForm, AnswerForm, UserCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from .models import Course,CourseMember,Message,ReplyMessage, Content, Answer, Score
from django.views .generic import (TemplateView, ListView,
                                    DetailView, CreateView,
                                    UpdateView, DeleteView,
                                    )
# Create your views here.
class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

class CourseListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = [Course, Content]
    template_name = 'course_list.html'
    def get_queryset(self):
        return Course.objects.raw('SELECT * FROM ertaapp_course INNER JOIN ertaapp_coursemember ON ertaapp_coursemember.course_id = ertaapp_course.id and ertaapp_coursemember.student_id=%s',[self.request.user.id])
    def get_context_data(self, **kwargs):
        context_data = super(CourseListView, self).get_context_data(**kwargs)
        context_data["my_special_key"] = Course.objects.raw('SELECT * FROM ertaapp_course where prof_id=%s',[self.request.user.id])
        context_data['messages_all'] = Answer.objects.raw('SELECT * FROM ertaapp_message where to_prof_id=%s ORDER BY create_date DESC',[self.request.user.id])
        context_data['crs'] = Course.objects.raw('SELECT * FROM ertaapp_course where prof_id=%s',[self.request.user.id])
        context_data['ans'] = Answer.objects.raw('SELECT * FROM ertaapp_answer')
        return context_data

class ContentListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Content
    template_name = 'content_list.html'
    def get_queryset(self):
        return Content.objects.raw('SELECT * FROM ertaapp_content where course_id=%s ORDER BY create_date DESC',[self.kwargs.get('pk')])
    def get_context_data(self, **kwargs):
        context = super(ContentListView, self).get_context_data(**kwargs)
        context['notif'] = Content.objects.raw('SELECT * FROM ertaapp_content where cat_id=2 and course_id=%s ORDER BY create_date DESC',[self.kwargs.get('pk')])
        context['tamrin'] = Content.objects.raw('SELECT * FROM ertaapp_content where cat_id=1 and course_id=%s ORDER BY create_date DESC',[self.kwargs.get('pk')])
        context['resource'] = Content.objects.raw('SELECT * FROM ertaapp_content where cat_id=3 and course_id=%s ORDER BY create_date DESC',[self.kwargs.get('pk')])
        context['crs'] = Course.objects.raw('SELECT * FROM ertaapp_course INNER JOIN ertaapp_coursemember ON  ertaapp_coursemember.student_id=%s and ertaapp_course.id=%s and ertaapp_coursemember.course_id = ertaapp_course.id',[self.request.user.id, self.kwargs.get('pk')])
        context['crs_admin'] = Course.objects.raw('SELECT * FROM ertaapp_course where ertaapp_course.id=%s and ertaapp_course.prof_id=%s',[self.kwargs.get('pk'), self.request.user.id])
        return context

class ContentDetailView(DetailView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Content
    template_name = 'content_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ContentDetailView, self).get_context_data(**kwargs)
        context['crs_admin'] = Course.objects.raw('SELECT * FROM ertaapp_course where ertaapp_course.id=%s and ertaapp_course.prof_id=%s',[self.kwargs.get('pk_alt'), self.request.user.id])
        context['crs'] = Course.objects.raw('SELECT * FROM ertaapp_course INNER JOIN ertaapp_coursemember ON ertaapp_coursemember.student_id=%s and ertaapp_course.id=%s and ertaapp_coursemember.course_id = ertaapp_course.id',[self.request.user.id, self.kwargs.get('pk_alt')])
        return context

class AdmincourseListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Course
    template_name = 'teacher_course_list.html'
    def get_queryset(self):
        return Course.objects.raw('SELECT * FROM ertaapp_course where prof_id=%s ORDER BY create_date DESC',[self.request.user.id])

class MessagecourseListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Message
    paginate_by = 5
    template_name = 'message_course_list.html'
    def get_queryset(self):
        return Message.objects.filter(course_id=self.kwargs.get('pk')).order_by('-create_date')
        # return Message.objects.raw('SELECT * FROM ertaapp_message where course_id=%s',[self.kwargs.get('pk')])
    def get_context_data(self, **kwargs):
        context = super(MessagecourseListView, self).get_context_data(**kwargs)
        context['crs_admin'] = Course.objects.raw('SELECT * FROM ertaapp_course where ertaapp_course.id=%s and ertaapp_course.prof_id=%s',[self.kwargs.get('pk'), self.request.user.id])
        return context

class StudentsListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Course
    paginate_by = 15
    template_name = 'students_list.html'
    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('pk'))
        # return Course.objects.raw('SELECT * FROM ertaapp_course where id=%s',[self.kwargs.get('pk')])
    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        context['crs_admin'] = Course.objects.raw('SELECT * FROM ertaapp_course where ertaapp_course.id=%s and ertaapp_course.prof_id=%s',[self.kwargs.get('pk'), self.request.user.id])
        return context


class ScontentListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Answer
    template_name = 'student_content.html'
    paginate_by = 5
    def get_queryset(self):
        return list(Answer.objects.raw('SELECT * FROM ertaapp_answer where author_id=%s and course_id=%s',[self.kwargs.get('pk'),self.kwargs.get('pk_alt')]))
    def get_context_data(self, **kwargs):
        context = super(ScontentListView, self).get_context_data(**kwargs)
        referer = self.request.META.get('HTTP_REFERER')
        context['purl'] = referer
        context['cnt'] = Answer.objects.raw('SELECT * FROM ertaapp_answer where author_id=%s and course_id=%s',[self.kwargs.get('pk'),self.kwargs.get('pk_alt')])
        context['crs_admin'] = Course.objects.raw('SELECT * FROM ertaapp_course where ertaapp_course.id=%s and ertaapp_course.prof_id=%s',[self.kwargs.get('pk_alt'), self.request.user.id])
        return context


class StudentanswerListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'student_answersall.html'
    context_object_name = 'answers_all'
    paginate_by = 5
    model = Answer
    def get_queryset(self):
        # return Answer.objects.filter(author_id=self.request.user.id).order_by('-create_date')
        return list(Answer.objects.raw('SELECT * FROM ertaapp_answer where author_id=%s ORDER BY create_date DESC',[self.request.user.id]))

class StudentmessageListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'student_messagesall.html'
    context_object_name = 'messages_all'
    model = Message
    paginate_by = 3
    def get_queryset(self):
        return Message.objects.filter(to_prof_id=self.request.user.id).order_by('-create_date')
        # return Message.objects.raw('SELECT * FROM ertaapp_message where to_prof_id=%s ORDER BY create_date DESC',[self.request.user.id])
    def get_context_data(self, **kwargs):
        context = super(StudentmessageListView, self).get_context_data(**kwargs)
        context['reps'] = ReplyMessage.objects.raw('SELECT * FROM ertaapp_replymessage')
        return context

class SendMessageView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'message_form.html'
    form_class = MessageForm
    model = Message
    # set username for author field
    def form_valid(self, form):
        message = form.save(commit=False)
        message.author = User.objects.get(username=self.request.user)  # use your own profile here
        course = self.request.POST['course']
        for x in Course.objects.raw('SELECT prof_id,id FROM ertaapp_course where id=%s',[course]):
            m = x.prof_id
        message.to_prof_id = m
        message.save()
        messages.success(self.request, 'پیام شما با موفقیت ارسال شد.')
        return redirect('course_list')
    def get_form_kwargs(self):
        kwargs = super(SendMessageView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class AddStudentView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'add_student.html'
    form_class = CourseMemberForm
    model = CourseMember
    def form_valid(self, form):
        student = form.save(commit=False)
        student.save()
        return redirect('course_list')
    def get_form_kwargs(self):
        kwargs = super(AddStudentView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class AddCourseView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'course_form.html'
    form_class = CourseForm
    model = Course
    def form_valid(self, form):
        course = form.save(commit=False)
        course.save()
        return redirect('teacher_course_list')

    def get_form_kwargs(self):
        kwargs = super(AddCourseView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class AddContentView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'add_content.html'
    form_class = ContentForm
    model = Content
    def form_valid(self, form):
        content = form.save(commit=False)
        content.save()
        return redirect('teacher_course_list')
    def get_form_kwargs(self):
        kwargs = super(AddContentView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class SetScoreView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'score_form.html'
    form_class = ScoreForm
    model = Score
    def form_valid(self, form):
        score = form.save(commit=False)
        score.course = Course.objects.get(id=self.kwargs.get('pk_alt'))
        score.student = CourseMember.objects.get(student_id=self.kwargs.get('pk'),course_id=self.kwargs.get('pk_alt'))
        score.save()
        return redirect('students_list', pk=self.kwargs.get('pk_alt'))

class ScoreUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'ertaapp/score_form.html'
    form_class = ScoreForm
    model = Score
    def get_success_url(self):
        return reverse('students_list', kwargs={'pk': self.kwargs.get('pk_alt')})

class CourseAnswersListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Answer
    paginate_by = 5
    template_name = 'all_answers_course.html'
    def get_context_data(self, **kwargs):
        context = super(CourseAnswersListView, self).get_context_data(**kwargs)
        referer = self.request.META.get('HTTP_REFERER')
        context['purl'] = referer
        context['cnt'] = Answer.objects.raw('SELECT * FROM ertaapp_answer where course_id=%s',[self.kwargs.get('pk')])
        context['crs_admin'] = Course.objects.raw('SELECT * FROM ertaapp_course where ertaapp_course.id=%s and ertaapp_course.prof_id=%s',[self.kwargs.get('pk'), self.request.user.id])
        return context


class AddAnswerView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'add_answer.html'
    redirect_field_name = 'next'
    form_class = AnswerForm
    model = Score
    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.save()
        return redirect('content_detail', pk=self.kwargs.get('pk'),pk_alt=self.kwargs.get('pk_alt'))
    def get_form_kwargs(self):
        kwargs = super(AddAnswerView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        kwargs.update(self.kwargs)
        return kwargs
    def get_context_data(self, **kwargs):
        context = super(AddAnswerView, self).get_context_data(**kwargs)
        context['crs'] = Course.objects.raw('SELECT * FROM ertaapp_course INNER JOIN ertaapp_coursemember ON ertaapp_coursemember.student_id=%s and ertaapp_course.id=%s and ertaapp_coursemember.course_id = ertaapp_course.id',[self.request.user.id, self.kwargs.get('pk_alt')])
        return context

class ContentUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'ertaapp/add_content.html'
    form_class = ContentForm
    model = Content
    def get_success_url(self):
        return reverse('content_detail', kwargs={'pk': self.kwargs.get('pk'), 'pk_alt': self.kwargs.get('pk_alt')})
    def get_form_kwargs(self):
        kwargs = super(ContentUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class ContentDeleteView(LoginRequiredMixin, DeleteView):
    model = Content
    success_url = reverse_lazy('teacher_course_list')

class ReplyMessageView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'reply_message_form.html'
    form_class = ReplyMessageForm
    model = ReplyMessage
    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.save()
        return redirect('student_messages')
    def get_form_kwargs(self):
        kwargs = super(ReplyMessageView, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs

class TeacherMessagesView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = ReplyMessage
    paginate_by = 5
    context_object_name = 'reply_all'
    template_name = 'teacher_messages.html'
    def get_queryset(self):
        return ReplyMessage.objects.filter(to_student_id=self.request.user.id).order_by('-create_date')
        # return ReplyMessage.objects.raw('SELECT * FROM ertaapp_replymessage where ertaapp_replymessage.to_student_id=%s',[self.request.user.id])
    def get_context_data(self, **kwargs):
        context = super(TeacherMessagesView, self).get_context_data(**kwargs)
        context['msg'] = Message.objects.raw('SELECT * FROM ertaapp_message where author_id=%s',[self.request.user.id])
        return context



class StudentsAnswersView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Answer
    paginate_by = 5
    context_object_name = 'answer_all'
    template_name = 'answers_all.html'
    def get_queryset(self):
        return Answer.objects.filter().order_by('-create_date')
        # return Answer.objects.raw('SELECT * FROM ertaapp_answer ORDER BY create_date DESC')
    def get_context_data(self, **kwargs):
        context = super(StudentsAnswersView, self).get_context_data(**kwargs)
        context['crs'] = Course.objects.raw('SELECT * FROM ertaapp_course where prof_id=%s ORDER BY create_date DESC',[self.request.user.id])
        return context

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'ertaapp/course_form.html'
    form_class = CourseForm
    model = Course
    def get_success_url(self):
        return reverse('course_list')
    def get_form_kwargs(self):
        kwargs = super(CourseUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')
