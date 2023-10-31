from django.db import models
# from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    login = models.CharField(max_length=100, default='', verbose_name='Логин')
    password = models.CharField(max_length=100, default='', verbose_name='Пароль')
    isModerator = models.BooleanField(default=False, verbose_name='Является модератором')

    class Meta:
        db_table = 'user'
        managed = True

class Application(models.Model):
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
    id_moderator = models.ForeignKey('User', on_delete=models.CASCADE,  db_column='id_moderator', related_name='moderator_application', blank=True, null=True)
    id_user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='id_user', related_name='user_application')

    class Meta:
        db_table = 'application'
        managed = True

class ApplicationSubscription(models.Model):
    id_application = models.ForeignKey('Application', models.DO_NOTHING, db_column='id_application')
    id_subscription = models.ForeignKey('Subscription', models.DO_NOTHING, db_column='id_subscription')

    class Meta:
        db_table = 'application_subscription'
        constraints = [
            models.UniqueConstraint(fields=['id_application', 'id_subscription'], name='composite_key')
        ]
        managed = True


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default='')
    STATUS_CHOICES = [
        ('enabled', 'enabled'),
        ('deleted', 'deleted'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='enabled')    

    class Meta:
        db_table = 'category'
        managed = True

class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0)
    info = models.TextField(default='')
    src = models.TextField(default='')
    id_category = models.ForeignKey('Category', models.DO_NOTHING, db_column='id_category', blank=True, null=True, related_name='subscription')
    STATUS_CHOICES = [
        ('enabled', 'enabled'),
        ('deleted', 'deleted'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'subscription'
        managed = True