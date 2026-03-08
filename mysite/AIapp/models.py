from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

class User(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=500)
    UserPassword = models.CharField(max_length=500)