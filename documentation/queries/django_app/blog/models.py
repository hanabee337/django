from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Post(models.Model):
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    modified_date = models.DateField(auto_now_add=True)
    author = models.ManyToManyField(Author)
    comments_count = models.IntegerField(default=0)
    pingback_count = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title
