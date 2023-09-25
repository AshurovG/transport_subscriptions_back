from django.db import models

class Users(models.Model):
    login = models.CharField(max_length=100, blank=True, null=True, verbose_name='Логин')
    password = models.CharField(max_length=100, blank=True, null=True, verbose_name='Пароль')

    class Meta:
        db_table = 'users'
        managed = True
