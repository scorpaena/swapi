from django.db import models


class StarWarsFilesModel(models.Model):

    file_name = models.CharField(max_length=250)
    url = models.URLField(max_length=250, default="https://swapi.dev/api/people/")
    date = models.DateField(auto_now_add=True)
