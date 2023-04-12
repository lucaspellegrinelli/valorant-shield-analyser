import json
import os


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
