from django.db import models


# Create your models here.
class Manufacturer(models.Model):
    title = models.CharField(max_length=100)

    # DB 에선
    # car(app 이름)_manufacturer(모델 클래스 이름. 소문자) 테이블이 생성되면, 속성들은
    # id 와 title이 생성

    def __str__(self):
        return self.title


class Car(models.Model):
    # 외래키는 _id가 붙음. 예) manufacturer_id DB sqlite3에서
    # 그래서, car_manufacturer(id)와 manufacturer_id(외래키)를
    # 연결시킨다.
    manufacturer = models.ForeignKey(Manufacturer)
    title = models.CharField(max_length=100)

    # car(app 이름)_car(모델클래스 이름. 소문자)) 테이블엔,
    # id, title, manufacturer_id(외래키)가 생성됨.

    def __str__(self):
        return '{} {}'.format(
            self.manufacturer.title,
            self.title
        )
