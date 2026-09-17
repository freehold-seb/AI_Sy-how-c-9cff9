import json
from pathlib import Path

import pytest

from scripts.file_organizer import (
    KNOWN_CATEGORIES,
    SCHEMA_PATH,
    classify_scanned_files,
    load_schema,
    main,
    scan_fixture_directory,
)


FIXTURE_DIRECTORY = Path(__file__).parent / "fixtures" / "file_organizer_scan"


def test_scan_fixture_directory_returns_names_and_extensions():
    assert scan_fixture_directory(FIXTURE_DIRECTORY) == [
        {"name": "notes.txt", "extension": ".txt"},
        {"name": "photo.JPG", "extension": ".jpg"},
        {"name": "README", "extension": ""},
        {"name": "song.MP3", "extension": ".mp3"},
    ]


def test_classify_scanned_files_maps_extensions_to_named_categories():
    scanned_files = scan_fixture_directory(FIXTURE_DIRECTORY)

    assert classify_scanned_files(scanned_files) == [
        {"name": "notes.txt", "extension": ".txt", "category": "document"},
        {"name": "photo.JPG", "extension": ".jpg", "category": "image"},
        {"name": "README", "extension": "", "category": "unknown"},
        {"name": "song.MP3", "extension": ".mp3", "category": "audio"},
    ]


def test_scan_fixture_directory_rejects_paths_outside_fixture_root(tmp_path):
    with pytest.raises(ValueError, match="tests/fixtures"):
        scan_fixture_directory(tmp_path)


def test_main_prints_fixture_names_extensions_and_categories(capsys):
    assert main([str(FIXTURE_DIRECTORY)]) == 0

    assert capsys.readouterr().out.splitlines() == [
        "notes.txt\t.txt\tdocument",
        "photo.JPG\t.jpg\timage",
        "README\t<none>\tunknown",
        "song.MP3\t.mp3\taudio",
    ]


def test_load_schema_maps_every_known_category_to_a_folder_name():
    schema = load_schema()

    assert schema.keys() == KNOWN_CATEGORIES
    for folder in schema.values():
        assert isinstance(folder, str) and folder.strip()


def test_load_schema_rejects_missing_category(tmp_path):
    incomplete = tmp_path / "schema.json"
    incomplete.write_text('{"document": "Documents"}', encoding="utf-8")

    with pytest.raises(ValueError, match="missing categories"):
        load_schema(incomplete)


def test_load_schema_rejects_unknown_category(tmp_path):
    schema = load_schema()
    invalid = {**schema, "video": "Videos"}
    bad_schema = tmp_path / "schema.json"
    bad_schema.write_text(json.dumps(invalid), encoding="utf-8")

    with pytest.raises(ValueError, match="unknown category"):
        load_schema(bad_schema)


def test_load_schema_rejects_blank_folder_name(tmp_path):
    schema = load_schema()
    invalid = {**schema, "unknown": "  "}
    bad_schema = tmp_path / "schema.json"
    bad_schema.write_text(json.dumps(invalid), encoding="utf-8")

    with pytest.raises(ValueError, match="non-empty string"):
        load_schema(bad_schema)


def test_schema_path_points_at_committed_schema_file():
    assert SCHEMA_PATH.name == "file_organizer_schema.json"
    assert SCHEMA_PATH.is_file()
