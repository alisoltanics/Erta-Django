from django.contrib import admin
from .models import Course,CourseMember,Message, Content, Answer, ContentCat, Score, ReplyMessage

admin.site.register(Course)
admin.site.register(CourseMember)
admin.site.register(Message)
admin.site.register(Content)
admin.site.register(Answer)
admin.site.register(ContentCat)
admin.site.register(Score)
admin.site.register(ReplyMessage)
