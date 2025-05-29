import json


def load_json(filepath: str) -> dict:
    """
    Load a JSON file and return its content as a dictionary.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file as a dictionary.
    """

    with open(filepath) as f:
        json_loaded = json.load(f)

    return json_loaded
