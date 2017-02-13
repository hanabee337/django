from django.contrib import admin

# Register your models here.
from .models import Choice, Question

#admin.site.register(Question)

# Part 7 : 관리자 폼 커스터마이징
#class QuestionAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,               {'fields': ['question_text']}),
#        ('Date information', {'fields': ['pub_date']}),
#    ]

#admin.site.register(Question, QuestionAdmin)

# Part 7 : 관련된 객체 추가
#admin.site.register(Choice)

# Part 7 : 관련된 객체 추가-2:
#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    list_display = ('question_text', 'pub_date', 'was_published_recently')
    
    # Part 7 : 관리자 변경 목록(change list) 커스터마이징
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)

