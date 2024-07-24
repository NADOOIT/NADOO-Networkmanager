import json


def write_to_file(file_path: str, content: str) -> None:
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)

