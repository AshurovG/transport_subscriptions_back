from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission, UserManager
from django.contrib.auth.models import User, PermissionsMixin , UserManager, AbstractBaseUser
# from django.contrib.postgres.fields import ArrayField

# class NewUserManager(UserManager):
#     def create_user(self,email,password=None, **extra_fields):
#         if not email:
#             raise ValueError('User must have an email address')
#         email = self.normalize_email(email) 
#         user = self.model(email=email, **extra_fields) 
#         user.set_password(password)
#         user.save(using=self.db)
#         return user

# class User(AbstractBaseUser, PermissionsMixin):
#     login = models.CharField(max_length=50, default='', verbose_name='Логин', unique=True)
#     email = models.EmailField(("email адрес"), unique=True)
#     password = models.CharField(max_length=50, verbose_name="Пароль")  
#     full_name = models.CharField(max_length=50, default='', verbose_name='ФИО')
#     phone_number = models.CharField(max_length=30, default='', verbose_name='Номер телефона')
#     is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
#     is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

#     USERNAME_FIELD = 'email'

#     objects =  NewUserManager()

class NewUserManager(UserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email) 
        user = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self.db)
        return user
    class Meta:
        managed = True

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(("email адрес"), unique=True)
    password = models.CharField(max_length=150, verbose_name="Пароль")    
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

    USERNAME_FIELD = 'email'

    objects =  NewUserManager()

    class Meta:
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
    id_moderator = models.ForeignKey('CustomUser', on_delete=models.CASCADE,  db_column='id_moderator', related_name='moderator_application', blank=True, null=True)
    id_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, db_column='id_user', related_name='user_application')

    class Meta:
        db_table = 'application'
        managed = False

class ApplicationSubscription(models.Model):
    id_application = models.ForeignKey('Application', models.DO_NOTHING, db_column='id_application')
    id_subscription = models.ForeignKey('Subscription', models.DO_NOTHING, db_column='id_subscription')

    class Meta:
        db_table = 'application_subscription'
        constraints = [
            models.UniqueConstraint(fields=['id_application', 'id_subscription'], name='composite_key')
        ]
        managed = False


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
        managed = False

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
        managed = False
        