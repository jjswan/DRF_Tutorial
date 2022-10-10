# Generated by Django 4.1.2 on 2022-10-07 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
