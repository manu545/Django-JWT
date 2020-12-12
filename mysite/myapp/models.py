from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.db import transaction

# Create your models here.

'''
class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username,and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        try:
            with transaction.atomic():
                user = self.model(username=username, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password=password, **extra_fields)
'''


class teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    subject = ArrayField(models.CharField(max_length=200), null=False)

    def __str__(self):
        return "{0}".format(self.username)

class student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    teacher = models.ForeignKey(teacher, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}".format(self.username)