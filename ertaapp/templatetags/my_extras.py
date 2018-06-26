from django import template
from ertaapp.models import Answer,Message,ReplyMessage
# this file is for creating our filters for use in html pages
import datetime
import re

register = template.Library()

@register.simple_tag
def my_tag(user):
    dans = Answer.objects.all().filter(author_id=user.id)
    dans = dans.count()
    return dans

register.filter('my_tag', my_tag)

@register.simple_tag
def dmes(user):
    dmes = Message.objects.all().filter(to_prof_id=user.id)
    dmes = dmes.count()
    return dmes

register.filter('dmes', dmes)

@register.simple_tag
def drep(user):
    drep = ReplyMessage.objects.all().filter(to_student_id=user.id)
    drep = drep.count()
    return drep

register.filter('drep', drep)

# @register.filter()
# def normal_text(value):
#     # x=['<p>','<br>','<b>','<h2>','<i>','<u>','<h1>','<h3>','<blockquote>','< >','<head>','<html>','<img>','table','style','class',]
#     # for i in x:
#     #     value = value.replace(i,' ')
#     value = value[0:141]
#     for i in value:
#         if re.search(r'[a-zA-Z]', i):
#             value = value.replace(i,' ')
#         if not i.isalpha():
#             value = value.replace(i,' ')
#     return value
#
# register.filter('normal_text', normal_text)
