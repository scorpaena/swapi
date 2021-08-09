# Generated by Django 2.2.12 on 2021-08-09 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StarWarsFilesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=250)),
                ('url', models.URLField(default='https://swapi.dev/api/people/', max_length=250)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]