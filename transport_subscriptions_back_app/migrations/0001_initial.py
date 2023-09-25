# Generated by Django 4.2.4 on 2023-09-25 20:26

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('registered', 'Зарегистрирован'), ('moderating', 'Проверяется'), ('approved', 'Принято'), ('denied', 'Отказано'), ('deleted', 'Удалено')], max_length=255, null=True)),
                ('creation_date', models.DateField(blank=True, null=True)),
                ('approving_date', models.DateField(blank=True, null=True)),
                ('publication_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'applications',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('src', models.TextField(blank=True, null=True)),
                ('info', models.TextField(blank=True, null=True)),
                ('rate_names', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=None)),
                ('rate_prices', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=None)),
                ('status', models.CharField(choices=[('enabled', 'enabled'), ('deleted', 'deleted')], max_length=255)),
            ],
            options={
                'db_table': 'subscriptions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(blank=True, max_length=100, null=True, verbose_name='Логин')),
                ('password', models.CharField(blank=True, max_length=100, null=True, verbose_name='Пароль')),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ApplicationsSubscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_applications', models.ForeignKey(blank=True, db_column='id_applications', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='transport_subscriptions_back_app.applications')),
                ('id_subscriptions', models.ForeignKey(blank=True, db_column='id_subscriptions', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='transport_subscriptions_back_app.subscriptions')),
            ],
            options={
                'db_table': 'applications_subscriptions',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='applications',
            name='id_moderator',
            field=models.ForeignKey(db_column='id_moderator', on_delete=django.db.models.deletion.CASCADE, related_name='moderator_applications', to='transport_subscriptions_back_app.users'),
        ),
        migrations.AddField(
            model_name='applications',
            name='id_user',
            field=models.ForeignKey(db_column='id_user', on_delete=django.db.models.deletion.CASCADE, related_name='user_applications', to='transport_subscriptions_back_app.users'),
        ),
    ]
