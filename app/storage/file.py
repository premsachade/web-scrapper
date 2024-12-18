import json
import os

from app.storage.base import Storage


class FileStorage(Storage):
    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path

    def save(self, data: dict) -> None:
        if os.path.exists(self.__file_path):
            with open(self.__file_path) as f:
                file_data: dict = json.load(f)
        else:
            file_data = {}

        file_data.update(data)

        with open(self.__file_path, "w+") as f:
            json.dump(file_data, f, indent=4)
