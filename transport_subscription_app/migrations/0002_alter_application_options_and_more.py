# Generated by Django 4.2.4 on 2023-11-12 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport_subscription_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='applicationsubscription',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'managed': False},
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default='', max_length=50, verbose_name='Почта'),
        ),
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(default='', max_length=50, verbose_name='ФИО'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='', max_length=30, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(default='', max_length=50, verbose_name='Логин'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=30, verbose_name='Пароль'),
        ),
    ]