from swapi.celery import app
from .services import StarWarsCSVFileProcessor


@app.task
def download_data_from_api(file_name):
    csv = CSVFileProcessor()
    csv.create_csv_file(file_name)
