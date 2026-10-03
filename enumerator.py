from abc import ABC, abstractmethod

import requests
from requests.exceptions import ConnectionError


class Enumerator(ABC):
    @abstractmethod
    def enumerate(self, file_path: str, url: str, extensions: list) -> dict:
        pass


class WebEnumerator(Enumerator):
    def enumerate(self, file_path, url, extensions=None):

        if extensions is None:
            extensions = [""]

        url = url.rstrip("/")
        endpoints = {}

        try:
            with open(file=file_path, mode="r") as f:
                for line in f:
                    word = line.strip()
                    if not word or word.startswith("#"):
                        continue

                    for ext in extensions:
                        if ext:
                            url_endpoint = url + "/" + word + "." + ext.lstrip(".")
                        else:
                            url_endpoint = url + "/" + word

                        response = requests.get(
                            url_endpoint, timeout=2, allow_redirects=False
                        )
                        if response.status_code != 404:
                            endpoints[url_endpoint] = response.status_code
        except FileNotFoundError:
            print("File not found, please check the path again.")
        except ConnectionError:
            print("Host is unavailable at the moment.")

        return endpoints
