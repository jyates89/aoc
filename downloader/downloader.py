import logging
from typing import List

import requests
from requests import cookies


class Downloader(object):
    INPUT_FILE_NAME: str = "aoc_input_{year}_{day}.txt"
    AOC_URL: str = "https://adventofcode.com/{year}/day/{day}/input"

    def __init__(self, *,  year: int, day: int, log_level: int = logging.INFO, cookie_list: List[tuple[str, str]]):
        if cookie_list is None:
            raise RuntimeError("AOC requires a session cookie to download the input files!")

        self._year = year
        self._day = day

        self._logging = logging.getLogger(Downloader.__name__)
        self._logging.setLevel(log_level)

        self._jar = cookies.RequestsCookieJar()
        for cookie in cookie_list:
            self._jar.set(*cookie)

        self._input_data: List[str] = []

    def download_input(self, *, destination: str) -> None:
        """
        Downloads the input data if needed, otherwise reads it from the existing file and stores it in input_data.
        """
        file_name = Downloader.INPUT_FILE_NAME.format(year=self._year, day=self._day)
        self._logging.info(f"Looking for input file {file_name} in {destination}.")
        try:
            with open(f"{destination}/{file_name}", 'r') as existing_file:
                lines = existing_file.readlines()
                for line in lines:
                    self._input_data.append(line)
            self._logging.info(f"Found and read file {file_name} in {destination}; input ready.")
        except FileNotFoundError:
            url = Downloader.AOC_URL.format(year=self._year, day=self._day)
            response = requests.get(url, cookies=self._jar)
            if response.status_code == 200:
                with open(f"{destination}/{file_name}", 'w') as output:
                    output.write(response.text)
                    for line in response.text.split('\n'):
                        self._input_data.append(line)
                self._logging.info(
                    f"Existing file was not found, downloaded {file_name} into {destination} successfully.")
            else:
                self._logging.error(f"Failed to download AOC input, {file_name}. Error: {response.status_code}.")

    @property
    def input_data(self) -> List[str]:
        return self._input_data
