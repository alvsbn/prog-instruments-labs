import json


def read_file(file_name: str) -> str:
    """
    Reads the contents of the file
    :param file_name: file name
    :return: file contents
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found")
    except IOError:
        raise IOError(f"Error reading file")
    except Exception as e:
        raise Exception("Error: {e}")


def read_json(file_name: str) -> dict:
    """
    Reads the contents of a json file
    :param file_name: file name
    :return: dictionary
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found")
    except IOError:
        raise IOError(f"Error reading file")
    except Exception as e:
        raise Exception("Error: {e}")


def write_json(file_name: str, text:float)->None:
    """
    Writes the content to a json file
    :param file_name: file naame
    :param text: text
    :return: None
    """
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(text, file, ensure_ascii=False, indent=4)
    except IOError:
        raise IOError(f"Couldn't write to a file")
    except Exception as e:
        raise Exception("Error: {e}")