from pathlib import Path

import pytest

from scripts.file_organizer import main, scan_fixture_directory


FIXTURE_DIRECTORY = Path(__file__).parent / "fixtures" / "file_organizer_scan"


def test_scan_fixture_directory_returns_names_and_extensions():
    assert scan_fixture_directory(FIXTURE_DIRECTORY) == [
        {"name": "notes.txt", "extension": ".txt"},
        {"name": "photo.JPG", "extension": ".jpg"},
        {"name": "README", "extension": ""},
    ]


def test_scan_fixture_directory_rejects_paths_outside_fixture_root(tmp_path):
    with pytest.raises(ValueError, match="tests/fixtures"):
        scan_fixture_directory(tmp_path)


def test_main_prints_fixture_names_and_extensions(capsys):
    assert main([str(FIXTURE_DIRECTORY)]) == 0

    assert capsys.readouterr().out.splitlines() == [
        "notes.txt\t.txt",
        "photo.JPG\t.jpg",
        "README\t<none>",
    ]
