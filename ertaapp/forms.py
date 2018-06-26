from django import forms
from .models import Course, CourseMember, ReplyMessage, Message, Content, Answer, Score
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
import datetime
from tinymce import TinyMCE

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('first_name', 'last_name', "username", "email", "password1", "password2", )
        model = get_user_model()
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    hellob = forms.CharField(required=False, widget=forms.HiddenInput)
    sem_code = forms.CharField(required=True)
    def clean_sem_code(self):
        sem_code = self.cleaned_data['sem_code']
        if sem_code != "semcs":
            raise forms.ValidationError('کد اشتباه است')
        return sem_code
    def clean_username(self):
        username = self.cleaned_data['username']
        username1=str(username)
        username1=username.lower()
        if User.objects.filter(username=username1).exists():
            self._errors["username"] = ErrorList([u"نام کاربری از قبل وجود دارد."])
        else:
            return username1
    def clean_hellob(self):
        hellob = self.cleaned_data['hellob']
        if len(hellob)>0:
            raise forms.ValidationError('heh')
        return hellob

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = " نام کاربری ( لطفا شامل نام و نام خانوادگی باشد. مثال: ali_soltani1996 )"
        self.fields["email"].label = "ایمیل"
        self.fields["first_name"].label = "نام (به فارسی)"
        self.fields["last_name"].label = "نام خانوادگی (به فارسی)"
        self.fields["sem_code"].label = " کد مورد نظر دانشگاه"

class CourseForm(forms.ModelForm):
    hellob = forms.CharField(required=False, widget=forms.HiddenInput)
    def clean_hellob(self):
        hellob = self.cleaned_data['hellob']
        if len(hellob)>0:
            raise forms.ValidationError('heh')
        return hellob

    def clean_picture(self):
        if len(self.request.FILES) != 0:
            picture = self.cleaned_data.get('picture')
            # 5MB - 5242880
            if picture._size > 4242880:
                raise forms.ValidationError(('حجم فایل باید کمتر از ۴ مگابایت باشد'))
            else:
                return picture

    class Meta():
        model = Course
        help_texts = {
            'picture': '',
        }
        fields = ('cname','year','term','prof','course_code','picture')
        labels = {
            'prof': ('استاد:'),
            'cname': ('نام درس:'),
            'year': ('سال تحصیلی:'),
            'term': ('ترم:'),
            'picture': ('تصویر:'),
            'course_code': ('کد درس (نمونه: db96)'),
            }
        widgets = {
        'prof':forms.Select(attrs={'class':'form-control'}),
        'picture':forms.FileInput(attrs={'id':'file1', 'style':'display:none'}),
        'cname':forms.TextInput(attrs={'class':'form-control'}),
        'year':forms.NumberInput(attrs={'class':'form-control'}),
        'term':forms.NumberInput(attrs={'class':'form-control'}),
        'course_code':forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CourseForm, self).__init__(*args,**kwargs)
        self.fields['prof'].queryset = User.objects.filter(username=request.user)
        self.initial['prof'] = request.user

class CourseMemberForm(forms.ModelForm):
    hellob = forms.CharField(required=False, widget=forms.HiddenInput)
    course_code1 = forms.CharField(required=True,)
    def clean_hellob(self):
        hellob = self.cleaned_data['hellob']
        if len(hellob)>0:
            raise forms.ValidationError('heh')
        return hellob
    def clean_course_code1(self):
        print (self.request.POST['course'])
        entered_code = self.cleaned_data['course_code1']
        print(entered_code)
        course_id = self.request.POST['course']
        course_code_org = Course.objects.filter(id=course_id,course_code=entered_code)
        code_org = course_code_org.values('course_code')
        x=1.1
        for course in code_org:
            x = course['course_code']
        if x != 1.1 :
            code_org = x
        if entered_code != code_org:
            raise forms.ValidationError('کد درس اشتباه است!')
        return entered_code

    class Meta():
        model=CourseMember
        fields = ('course','course_code1','student')
        labels = {
            'course': ('درس:'),
            }
        widgets = {
        'course':forms.Select(attrs={'class':'form-control'}),
        'course_code1':forms.TextInput(attrs={'class':'form-control'}),
        'student':forms.HiddenInput(attrs={'class':'form-control'}),
        }
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CourseMemberForm, self).__init__(*args,**kwargs)
        self.fields['course'].queryset = Course.objects.filter()
        self.fields["course_code1"].label = "کد درس"
        self.fields['student'].queryset = User.objects.filter(username=request.user)
        self.initial['student'] = request.user


# prof_id=request.user.id

class ReplyMessageForm(forms.ModelForm):
    hellob = forms.CharField(required=False, widget=forms.HiddenInput)
    def clean_hellob(self):
        hellob = self.cleaned_data['hellob']
        if len(hellob)>0:
            raise forms.ValidationError('heh')
        return hellob

    class Meta():
        model=ReplyMessage
        fields = ('text','message','to_student')
        widgets = {
        'text':TinyMCE(attrs={'class':'form-control'}),
        'message':forms.HiddenInput(attrs={'class':'form-control'}),
        'to_student':forms.HiddenInput(attrs={'class':'form-control'}),
        }
        labels = {
            'text': ('متن پیام:'),
            }
    def __init__(self, pk=None, pk_alt=None, *args, **kwargs):
        super(ReplyMessageForm, self).__init__(*args,**kwargs)
        self.fields['message'].queryset = Message.objects.filter(id=pk)
        self.fields['to_student'].queryset = User.objects.filter(id=pk_alt)
        self.initial['message'] = pk
        self.initial['to_student'] = pk_alt

class MessageForm(forms.ModelForm):

    class Meta():
        model=Message
        fields = ('course','title', 'text')
        labels = {
            'course': ('درس:'),
            'title': ('عنوان:'),
            'text': ('متن:'),
            }
        widgets = {
        'course':forms.Select(attrs={'class':'form-control'}),
        'title':forms.TextInput(attrs={'class':'form-control'}),
        'text':TinyMCE(attrs={'class':'form-control'}),
        }


    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(MessageForm, self).__init__(*args,**kwargs)
        m = []
        for x in Course.objects.raw('SELECT ertaapp_course.id FROM ertaapp_course INNER JOIN ertaapp_coursemember ON ertaapp_coursemember.course_id = ertaapp_course.id and ertaapp_coursemember.student_id=%s',[request.user.id]):
            m.append(x.id)
        m = tuple(m)
        self.fields['course'].queryset = Course.objects.filter(id__in=m)



class ContentForm(forms.ModelForm):

    hellob = forms.CharField(required=False, widget=forms.HiddenInput)
    def clean_hellob(self):
        hellob = self.cleaned_data['hellob']
        if len(hellob)>0:
            raise forms.ValidationError('heh')
        return hellob

    def clean_file_tamrin(self):
        file_tamrin = self.cleaned_data.get('file_tamrin')
        # 5MB - 5242880
        if file_tamrin != None:
            if file_tamrin._size > 4242880:
                self._errors["file_tamrin"] = ErrorList([u"حجم فایل باید کمتر از ۴ مگابایت باشد."])
            else:
                return (file_tamrin)
    class Meta():
        model=Content
        fields = ('title','author','course','cat', 'text', 'due', 'file_tamrin',)
        labels = {
            'course': ('درس:'),
            'title': ('عنوان:'),
            'text': ('متن:'),
            'cat': ('دسته:'),
            'author': ('استاد:'),
            'file_tamrin': ('فایل:'),
            'due': ('تاریخ پایان مهلت ارسال پاسخ (اگر محتوا تمرین است):')
            }
        widgets = {
        'course':forms.Select(attrs={'class':'form-control'}),
        'author':forms.Select(attrs={'class':'form-control'}),
        'cat':forms.Select(attrs={'class':'form-control'}),
        'file_tamrin':forms.FileInput(attrs={'id':'file1', 'style':'display:none'}),
        'title':forms.TextInput(attrs={'class':'form-control'}),
        'text':TinyMCE(mce_attrs={'class':'form-control',}),
        'due':forms.SelectDateWidget(attrs={'class':'form-control'}),
        }

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ContentForm, self).__init__(*args,**kwargs)
        self.fields['course'].queryset = Course.objects.filter(prof_id=request.user.id)
        self.fields['author'].queryset = User.objects.filter(username=request.user)
        self.initial['author'] = request.user

class ScoreForm(forms.ModelForm):
    hellob = forms.CharField(required=False, widget=forms.HiddenInput)
    def clean_hellob(self):
        hellob = self.cleaned_data['hellob']
        if len(hellob)>0:
            raise forms.ValidationError('heh')
        return hellob

    class Meta():
        model=Score
        fields = ('score',)
        labels = {
            'score': ('نمره‌ی میانترم:'),
            }
        widgets = {
        'score':forms.NumberInput(attrs={'class':'form-control'}),
        }

class AnswerForm(forms.ModelForm):
    hellob = forms.CharField(required=False, widget=forms.HiddenInput)
    def clean_hellob(self):
        hellob = self.cleaned_data['hellob']
        if len(hellob)>0:
            raise forms.ValidationError('heh')
        return hellob
    def clean_file_ta(self):
        file_ta = self.cleaned_data.get('file_ta')
        # 5MB - 5242880
        if file_ta._size > 4242880:
            self._errors["file_ta"] = ErrorList([u"حجم فایل باید کمتر از ۴ مگابایت باشد."])
        else:
            return (file_ta)

    def clean_content(self):
        content_pk = self.pk
        content = self.cleaned_data.get('content')
        due = Content.objects.filter(id=content_pk)
        due = due.values('due')
        x=1.1
        for s in due:
            x = s['due']
        x = str(x)
        current_date = str(datetime.datetime.today().strftime('%Y-%m-%d'))
        if x <= current_date:
            self._errors["file_ta"] = ErrorList([u"مهلت ارسال پاسخ تمرین تمام شده است!"])
        return content

    class Meta():
        model=Answer
        fields = ('text','author','course','content', 'file_ta')
        labels = {
                    'course': ('درس:'),
                    'text': ('متن:'),
                    'content': ('تمرین:'),
                    'author': ('دانشجو:'),
                    'file_ta': ('فایل پاسخ (الزامی):'),
                    }
        widgets = {
                'course':forms.HiddenInput(attrs={'class':'form-control'}),
                'author':forms.HiddenInput(attrs={'class':'form-control'}),
                'content':forms.HiddenInput(attrs={'class':'form-control'}),
                'text':TinyMCE(attrs={'class':'form-control'}),
                'file_ta':forms.FileInput(attrs={'id':'file1', 'style':'display:none'}),
                }

    def __init__(self, request, pk=None, pk_alt=None, *args, **kwargs):
        self.request = request
        self.pk = pk
        super(AnswerForm, self).__init__(*args,**kwargs)
        self.fields['course'].queryset = Course.objects.filter(id=pk_alt)
        self.initial['author'] = request.user
        self.fields['content'].queryset = Content.objects.filter(id=pk)
        self.initial['content'] = pk
        self.initial['course'] = pk_alt
