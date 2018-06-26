from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group


# Create your models here.

# def get_first_name(self):
#     return self.username + ' (' + self.first_name +' '+ self.last_name + ')'
# User.add_to_class("__str__", get_first_name)

class Course(models.Model):
    prof = models.ForeignKey('auth.User',related_name='professor',verbose_name="استاد")
    cname = models.CharField(max_length=100,verbose_name="نام")
    year = models.IntegerField(default=1396)
    term = models.IntegerField(default=2)
    create_date = models.DateTimeField(default=timezone.now)
    students = models.ManyToManyField('auth.User',through='CourseMember')
    picture = models.ImageField(upload_to="course_pics",default='course_pics/default_course.png', blank=True)
    course_code = models.CharField(unique=True, max_length=15,verbose_name="کد درس")
    def __str__(self):
        return self.cname + " >> "+ str(self.prof.last_name)
    class Meta:
        verbose_name="درسی"
        unique_together = ["cname", "prof"]

class CourseMember(models.Model):
    student = models.ForeignKey('auth.User',verbose_name='نام')
    course = models.ForeignKey('ertaapp.Course',related_name='members',verbose_name='درس')
    def __str__(self):
        return str(self.student)+' > '+str(self.course)
    class Meta:
        verbose_name="عضوی"
        unique_together = ["student", "course"]


class Message(models.Model):
    author = models.ForeignKey('auth.User',related_name='message_author')
    to_prof = models.ForeignKey('auth.User')
    course = models.ForeignKey('ertaapp.Course',related_name='messages')
    title = models.CharField(max_length=100)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title


class ReplyMessage(models.Model):
    message = models.ForeignKey('ertaapp.Message',related_name='replies')
    text = models.TextField()
    to_student = models.ForeignKey('auth.User')
    create_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.message)

class Content(models.Model):
    author = models.ForeignKey('auth.User',related_name='content_author',verbose_name='استاد')
    course = models.ForeignKey('ertaapp.Course',verbose_name='درس')
    cat = models.ForeignKey('ertaapp.ContentCat',verbose_name='دسته')
    title = models.CharField(max_length=100,verbose_name='عنوان')
    text = models.TextField()
    due = models.DateField(default=timezone.now, blank=True)
    file_tamrin = models.FileField(upload_to='content_files', blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name="محتوایی"
        unique_together = ["author", "course", "cat", "title"]

class Answer(models.Model):
    author = models.ForeignKey('auth.User',related_name='answer_author',verbose_name=" نام دانشجو ")
    content = models.ForeignKey('ertaapp.Content', related_name='answers',verbose_name=" نام تمرین ")
    course = models.ForeignKey('ertaapp.Course', null=True,verbose_name=" نام درس ", related_name='answers')
    text = models.TextField()
    file_ta = models.FileField(upload_to='answer_files')
    create_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.content)+' by '+str(self.author)
    class Meta:
        verbose_name='تمرینی'
        unique_together = ["author", "course", "content"]

class ContentCat(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Score(models.Model):
    student = models.ForeignKey('ertaapp.CourseMember',related_name='stud_scores')
    course = models.ForeignKey('ertaapp.Course',related_name='scores')
    score = models.FloatField(default=20)
    def __str__(self):
        return str(self.score)

# Set group and active new user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='student'))
        user = User.objects.get(pk=instance.pk)
        user.is_staff = True
        user.is_active = True
        user.save()
