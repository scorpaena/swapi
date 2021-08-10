import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from data_parser.models import StarWarsFilesModel


today = date.today()


@pytest.fixture
def user(db):
    return User.objects.create(username="foo", password="bar123$%")


@pytest.fixture
def people(db):
    return StarWarsFilesModel.objects.create(
        file_name="bar",
        url="https://swapi.dev/api/people/",
    )


@pytest.fixture
def client(user):
    return APIClient()


# def test_starwars_list_view(client, people):
#     request = client.get("/api/files/")
#     assert request.status_code == 200
#     assert request.data["count"] == 1


# def test_starwars_create_view(client):
#     request = client.post("/api/files/")
#     assert request.status_code == 201
#     assert StarWarsFilesModel.objects.last().file_name.startswith("people") == True
