from django.db import models
from django.contrib.postgres.fields import ArrayField

class Users(models.Model):
    login = models.CharField(max_length=100, blank=True, null=True, verbose_name='Логин')
    password = models.CharField(max_length=100, blank=True, null=True, verbose_name='Пароль')

    class Meta:
        db_table = 'users'
        managed = True

class Applications(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Зарегистрирован'),
        ('moderating', 'Проверяется'),
        ('approved', 'Принято'),
        ('denied', 'Отказано'),
        ('deleted', 'Удалено')
    ]
    status = models.CharField(max_length=255, blank=True, null=True, choices=STATUS_CHOICES)
    creation_date = models.DateField(blank=True, null=True)
    approving_date = models.DateField(blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    id_moderator = models.ForeignKey('Users', on_delete=models.CASCADE,  db_column='id_moderator', related_name='moderator_applications')
    id_user = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='id_user', related_name='user_applications')

    class Meta:
        managed = True
        db_table = 'applications'


class ApplicationsSubscriptions(models.Model):
    id_applications = models.ForeignKey('Applications', models.DO_NOTHING, db_column='id_applications', blank=True, null=True)
    id_subscriptions = models.ForeignKey('Subscriptions', models.DO_NOTHING, db_column='id_subscriptions', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'applications_subscriptions'


class Subscriptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    src = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    rate_names = ArrayField(models.TextField(blank=True, null=True))
    rate_prices = ArrayField(models.TextField(blank=True, null=True))

    STATUS_CHOICES = [
        ('enabled', 'enabled'),
        ('deleted', 'deleted'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    class Meta:
        managed = True
        db_table = 'subscriptions'