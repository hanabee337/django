from django.db import models


class Topping(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Pizza(models.Model):
    title = models.CharField(max_length=100)
    # ManyToMany 관계에서는 아무나 역참조가 되지만,
    # 포함관계에서 상위요소에 해당하는 클래스에 ManyToMany를 선언한다.
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return '{}, (Toppings : {})'.format(
            self.title,
            ','.join(self.toppings.values_list('title', flat=True))
        )


