from django.db import models


class Topping(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Pizza(models.Model):
    title = models.CharField(max_length=100)
    # Pizza와 Topping은 서로 ManyToMany 관계
    # ManyToMany 관계에서는 아무나 역참조가 되지만,
    # 포함관계에서 상위요소에 해당하는 클래스에 ManyToMany를 선언한다.
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return '{}, (Toppings : {})'.format(
            self.title,
            ','.join(self.toppings.values_list('title', flat=True))
        )
    # flat = True로 하면, tutple이지만, 인자가 하나밖에 없는 경우,
    # flat=True로 해서, list로 뽑아올 수 있다.
    # If you only pass in a single field, you can also pass in the flat parameter.
    # If True, this will mean the returned results are single values,
    # rather than one-tuples.



