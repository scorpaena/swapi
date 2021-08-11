import requests
from datetime import datetime
import csv
import re
import os
from urllib.parse import urljoin
from django.core.exceptions import ObjectDoesNotExist
from .exceptions import DoesNotExistError
from .models import StarWarsFilesModel


class StarWarsAPIClient:
    def __init__(self):
        self.base_url = "https://swapi.py4e.com/api/"

    def _item_url_to_id(self, url):
        match = re.search(r"\d+/$", url) or re.search(r"\d+$", url)
        if match is None:
            raise ValueError(f"{url} doesn't contain item ID")
        id = url[match.start() : match.end()]
        if "/" in id:
            id = id.replace("/", "")
        return id

    def _resource_url_generator(self, resource):
        return urljoin(self.base_url, resource)

    def _item_url_generator(self, resource, id):
        resource_path = self._resource_url_generator(resource)
        return urljoin(resource_path, str(id))

    def _item_url_list_to_id_list(self, url_list):
        id_list = []
        if len(url_list) != 0:
            for url in url_list:
                id_list.append(self._item_url_to_id(url))
        return id_list

    def _people_result_substitutor(self, item):
        result_dict = {}
        for key in item:
            result_dict[key] = item[key]
            result_dict["homeworld"] = self._item_url_to_id(url=item["homeworld"])
            result_dict["films"] = self._item_url_list_to_id_list(
                url_list=item["films"]
            )
            result_dict["species"] = self._item_url_list_to_id_list(
                url_list=item["species"]
            )
            result_dict["vehicles"] = self._item_url_list_to_id_list(
                url_list=item["vehicles"]
            )
            result_dict["starships"] = self._item_url_list_to_id_list(
                url_list=item["starships"]
            )
        return result_dict

    def _get_object_by_id(self, resource, id):
        url = self._item_url_generator(resource, id)
        response = requests.get(url)
        if response.status_code != 200:
            raise DoesNotExistError(url)
        return response.json()

    def _get_lookup_value(self, resource, lookup_key, id):
        value = self._get_object_by_id(resource, id).get(lookup_key)
        if value is None:
            raise KeyError(f"item #{id} does not have '{lookup_key}' attribute")
        return value

    def _get_lookup_values_list(self, resource, lookup_key, id):
        values_list = []
        for item in id:
            values_list.append(self._get_lookup_value(resource, lookup_key, id=item))
        return values_list

    def _get_data_per_page(self, page_number, resource):
        page_url = self._resource_url_generator(resource)
        response = requests.get(page_url, params={"page": page_number}).json()
        results = response.get("results")
        if results is None:
            raise KeyError(f"{resource} does not have 'results' attribute")
        elif len(results) == 0:
            raise ValueError(f"'results' list is empty")
        else:
            new_result = []
            for item in results:
                new_result.append(self._people_result_substitutor(item))
            response["results"] = new_result
        return response

    def _get_data_all(self, resource):
        page_number = 1
        next_page = True
        while next_page is not None:
            response = self._get_data_per_page(page_number, resource)
            page_number += 1
            next_page = response["next"]
            for item in response["results"]:
                yield item

    def get_planets_detail(self, id, resource="planets/", lookup_key="name"):
        return self._get_lookup_value(resource, lookup_key, id)

    def get_films_detail(self, id, resource="films/", lookup_key="title"):
        return self._get_lookup_values_list(resource, lookup_key, id)

    def get_species_detail(self, id, resource="species/", lookup_key="name"):
        return self._get_lookup_values_list(resource, lookup_key, id)

    def get_vehicles_detail(self, id, resource="vehicles/", lookup_key="name"):
        return self._get_lookup_values_list(resource, lookup_key, id)

    def get_starships_detail(self, id, resource="starships/", lookup_key="name"):
        return self._get_lookup_values_list(resource, lookup_key, id)

    def get_people_per_page(self, page_number, resource="people/"):
        return self._get_data_per_page(page_number, resource)

    def get_people_all(self, resource="people/"):
        return self._get_data_all(resource)


class StarWarsAPIDataProcessor:
    def __init__(self):
        self.api_client = StarWarsAPIClient()

    def people_all_data_set(self):
        data = self.api_client.get_people_all()
        for item in data:
            result_dict = item
            result_dict["homeworld"] = self.api_client.get_planets_detail(
                id=item["homeworld"]
            )
            result_dict["films"] = self.api_client.get_films_detail(id=item["films"])
            result_dict["species"] = self.api_client.get_species_detail(
                id=item["species"]
            )
            result_dict["vehicles"] = self.api_client.get_vehicles_detail(
                id=item["vehicles"]
            )
            result_dict["starships"] = self.api_client.get_starships_detail(
                id=item["starships"]
            )
            yield result_dict


class CSVFileProcessor:
    def __init__(self):
        self.data_processor = StarWarsAPIDataProcessor()
        self.file_folder_path = "data_parser/csv_files/"
        self.csv_columns = [
            "name",
            "height",
            "mass",
            "hair_color",
            "skin_color",
            "eye_color",
            "birth_year",
            "gender",
            "homeworld",
            "films",
            "species",
            "vehicles",
            "starships",
            "created",
            "edited",
            "url",
        ]

    def _get_file_name(self, id):
        try:
            object = StarWarsFilesModel.objects.get(id=id)
        except ObjectDoesNotExist as error:
            raise error
        return object.file_name

    def _get_file_path(self, id):
        file_name = self._get_file_name(id)
        path = f"{self.file_folder_path}{file_name}"
        is_file = os.path.isfile(path)
        if not is_file:
            raise FileNotFoundError(f"{file_name} is not found")
        return path

    def create_csv_file(self, file_name):
        data_to_save = self.data_processor.people_all_data_set()
        with open(f"data_parser/csv_files/{file_name}", "w") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.csv_columns)
            csv_writer.writeheader()
            for item in data_to_save:
                csv_writer.writerow(item)

    def read_from_csv_file(self, id):
        path = self._get_file_path(id)
        with open(path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for item in csv_reader:
                yield item


def csv_file_name():
    now = datetime.now().strftime("%m-%d-%y %H:%M:%S")
    return f"people_{now}.csv"
