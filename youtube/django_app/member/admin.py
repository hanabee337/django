from django.contrib import admin

# Register your models here.
from member.models import MyUser

# 이렇게만 하면 admin이 잘 동작하지 않음
# admin에서 다 설정을 해줘야 함.
# 즉, django customuser를 admin에 등록을 해줄 필요가 있음
# django customuser admin으로 goolging
admin.site.register(MyUser)