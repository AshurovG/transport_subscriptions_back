# Generated by Django 4.2.4 on 2023-12-19 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport_subscription_app', '0004_alter_subscription_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='active_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]