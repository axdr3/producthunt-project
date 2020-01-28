import re
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):

    url = models.TextField()
    image = models.ImageField(upload_to="images/")
    icon = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=20)
    body = models.TextField()
    pub_date = models.DateTimeField()
    votes_total = models.IntegerField(default=1)
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def populate(self, title, body, url, image, icon):
        self.url = url
        self.title = title
        self.image = image
        self.icon = icon
        self.body = body



    def __str__(self):
        return self.title

    def isValidURL(self):
        if self.url.startswith('http://') or self.url.startswith('https://'):
            return True
        return False

    def summary(self):
        return self.body[:150] + '...'

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')
