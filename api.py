import json
import logging
import os

import requests


def cache_wrapper(cache_path: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if os.path.exists(cache_path):
                with open(cache_path, "r") as f:
                    return json.load(f)

            response = func(*args, **kwargs)

            if response.status_code == 200:
                with open(cache_path, "w") as f:
                    json.dump(response.json(), f)

            return response.json()

        return wrapper

    return decorator


class APIRequester:
    BASE_PATH = "https://api.henrikdev.xyz/valorant"

    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        self.logger = logging.getLogger(__name__)

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def get_details(self, name: str, tag: str):
        details_cache_path = os.path.join(self.cache_dir, f"{name}-{tag}-details.json")

        @cache_wrapper(details_cache_path)
        def get_details():
            self.logger.info(f"Fetching details for {name}#{tag}...")
            response = requests.get(f"{self.BASE_PATH}/v1/account/{name}/{tag}")
            response.raise_for_status()
            return response

        return get_details()

    def get_matches(self, name: str, tag: str, region: str):
        player_details = self.get_details(name, tag)
        player_id = player_details["data"]["puuid"]

        matches_cache_path = os.path.join(self.cache_dir, f"{name}-{tag}-matches.json")

        @cache_wrapper(matches_cache_path)
        def get_matches():
            self.logger.info(f"Fetching matches for {name}#{tag}...")
            response = requests.get(
                f"{self.BASE_PATH}/v3/by-puuid/matches/{region}/{player_id}?filter=competitive&size=10"
            )
            response.raise_for_status()
            return response

        return get_matches()
