from django.contrib import admin

from .models import Question, Choice


# admin.site.register(Question)
# Customize the admin form
class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None,              {'fields': ['question_text']}),
        ('Date Information',{'fields': ['pub_date']}),
    ]
admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)
