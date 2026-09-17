from pathlib import Path

import pytest

from scripts.file_organizer import classify_scanned_files, main, scan_fixture_directory


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
