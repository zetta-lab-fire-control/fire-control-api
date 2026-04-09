import json

from pathlib import Path


description_path: Path = Path(__file__).parent / "docs/description.md"
version_path: Path = Path(__file__).parent / "docs/version.txt"
tags_path: Path = Path(__file__).parent / "docs/tags.json"


def load_api_metadata():
    try:
        api_version = version_path.read_text(encoding="utf-8").strip()

    except FileNotFoundError:
        api_version = "0.0.0"

    try:
        api_description = description_path.read_text(encoding="utf-8").strip()

    except FileNotFoundError:
        api_description = ""

    try:
        tags_content = tags_path.read_text(encoding="utf-8").strip()

        api_tags = json.loads(tags_content) if tags_content else []

    except (FileNotFoundError, json.JSONDecodeError):
        api_tags = []

    return {
        "api_version": api_version,
        "api_description": api_description,
        "api_tags": api_tags,
    }


api_metadata = load_api_metadata()
