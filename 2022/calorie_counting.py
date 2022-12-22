import logging

import requests
from requests import cookies
from typing import List


class CalorieCounting(object):
    OUTPUT: str = "calories_input.txt"

    def __init__(self, log_level: int, cookie_list: List[tuple[str, str]]):
        self.logging = logging.getLogger(CalorieCounting.__name__)
        self.logging.setLevel(log_level)

        self.jar = cookies.RequestsCookieJar()
        for cookie in cookie_list:
            self.jar.set(*cookie)

        self.calories = []

    def download_input(self, url: str):
        try:
            with open(CalorieCounting.OUTPUT, 'r') as existing_file:
                lines = existing_file.readlines()
                for line in lines:
                    self.calories.append(line)
            self.logging.info("Found and read file.")
        except FileNotFoundError:
            response = requests.get(url, cookies=self.jar)
            with open(CalorieCounting.OUTPUT, 'w') as output:
                output.write(response.text)
                for line in response.text.split('\n'):
                    self.calories.append(line)
            self.logging.info("File not found, downloaded new copy.")

    def calculate_max_of_all(self):
        total = 0
        groups = []
        for entry in self.calories:
            if entry.strip().isnumeric():
                total += int(entry)
            else:
                groups.append(total)
                total = 0
        highest_calories_carried = max(groups)
        self.logging.info(f'Highest amount carried: {highest_calories_carried}.')

    def calculate_max_of_top_three(self):
        total = 0
        groups = []
        for entry in self.calories:
            if entry.strip().isnumeric():
                total += int(entry)
            else:
                groups.append(total)
                total = 0

        sorted_groups = sorted(groups)

        highest_calories_carried = sorted_groups[-1]
        self.logging.info(f'Highest amount carried: {highest_calories_carried}.')

        second_highest_calories_carried = sorted_groups[-2]
        self.logging.info(f'Second highest amount carried: {second_highest_calories_carried}.')

        third_highest_calories_carried = sorted_groups[-3]
        self.logging.info(f'Third highest amount carried: {third_highest_calories_carried}.')

        total_of_top_three = highest_calories_carried + second_highest_calories_carried + third_highest_calories_carried
        self.logging.info(f'Total of top three: {total_of_top_three}.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, format="%(asctime)s: %(levelname)s: %(name)s: %(lineno)d: %(message)s",
                        datefmt="%Y-%m-%dT%H:%M:%S%z")
    calorie_counter = CalorieCounting(logging.INFO, [
        ('session',
         ''),
    ])
    calorie_counter.download_input("https://adventofcode.com/2022/day/1/input")
    calorie_counter.calculate_max_of_all()
    calorie_counter.calculate_max_of_top_three()
