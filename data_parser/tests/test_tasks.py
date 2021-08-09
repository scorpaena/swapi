from swapi.celery import app
from data_parser.tasks import download_data_from_api
import pytest


@pytest.fixture
def celery_app(request):
    app.conf.update(CELERY_ALWAYS_EAGER=True)
    return app


def test_task(celery_app):
    file_name = "people"
    download_data_from_api.delay(file_name)
