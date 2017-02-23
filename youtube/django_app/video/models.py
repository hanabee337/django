from django.db import models


# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    published_date = models.DateTimeField()
    youtube_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title
