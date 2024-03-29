# Generated by Django 4.0.2 on 2022-02-23 15:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_sympathy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sympathy',
            options={'verbose_name_plural': 'Sympathies'},
        ),
        migrations.AlterField(
            model_name='sympathy',
            name='like',
            field=models.ManyToManyField(related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
