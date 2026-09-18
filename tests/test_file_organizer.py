import json
from pathlib import Path

import pytest

from scripts.file_organizer import (
    KNOWN_CATEGORIES,
    SCHEMA_PATH,
    classify_scanned_files,
    execute_moves,
    load_schema,
    main,
    plan_moves,
    scan_fixture_directory,
    validate_moves,
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


def test_plan_moves_maps_classified_files_to_schema_destinations():
    classified_files = classify_scanned_files(scan_fixture_directory(FIXTURE_DIRECTORY))
    planned_moves = plan_moves(classified_files, load_schema(), FIXTURE_DIRECTORY)

    assert planned_moves == [
        {
            "name": "notes.txt",
            "category": "document",
            "source": FIXTURE_DIRECTORY.resolve() / "notes.txt",
            "destination": FIXTURE_DIRECTORY.resolve() / "Documents" / "notes.txt",
            "conflict": False,
        },
        {
            "name": "photo.JPG",
            "category": "image",
            "source": FIXTURE_DIRECTORY.resolve() / "photo.JPG",
            "destination": FIXTURE_DIRECTORY.resolve() / "Images" / "photo.JPG",
            "conflict": False,
        },
        {
            "name": "README",
            "category": "unknown",
            "source": FIXTURE_DIRECTORY.resolve() / "README",
            "destination": FIXTURE_DIRECTORY.resolve() / "unsorted" / "README",
            "conflict": False,
        },
        {
            "name": "song.MP3",
            "category": "audio",
            "source": FIXTURE_DIRECTORY.resolve() / "song.MP3",
            "destination": FIXTURE_DIRECTORY.resolve() / "Audio" / "song.MP3",
            "conflict": False,
        },
    ]


def test_main_dry_run_prints_planned_moves(capsys):
    assert main([str(FIXTURE_DIRECTORY), "--dry-run"]) == 0

    assert capsys.readouterr().out.splitlines() == [
        "notes.txt -> Documents\\notes.txt",
        "photo.JPG -> Images\\photo.JPG",
        "README -> unsorted\\README",
        "song.MP3 -> Audio\\song.MP3",
    ]


def test_plan_moves_routes_existing_destination_to_unsorted(tmp_path):
    source = tmp_path / "scan"
    source.mkdir()
    (source / "notes.txt").write_text("incoming", encoding="utf-8")
    (source / "Documents").mkdir()
    (source / "Documents" / "notes.txt").write_text("existing", encoding="utf-8")

    planned = plan_moves(
        [{"name": "notes.txt", "extension": ".txt", "category": "document"}],
        load_schema(),
        source,
    )

    assert planned[0]["destination"] == source / "unsorted" / "notes.txt"
    assert planned[0]["conflict"] is True


def test_main_dry_run_marks_existing_destination_conflict(tmp_path, capsys, monkeypatch):
    source = tmp_path / "scan"
    source.mkdir()
    (source / "notes.txt").write_text("incoming", encoding="utf-8")
    (source / "Documents").mkdir()
    (source / "Documents" / "notes.txt").write_text("existing", encoding="utf-8")
    monkeypatch.setattr("scripts.file_organizer.FIXTURES_ROOT", tmp_path.resolve())

    assert main([str(source), "--dry-run"]) == 0

    assert capsys.readouterr().out.splitlines() == [
        "notes.txt -> unsorted\\notes.txt [CONFLICT -> unsorted]",
    ]


def test_main_dry_run_does_not_modify_fixture_directory(capsys):
    before = sorted(path.relative_to(FIXTURE_DIRECTORY) for path in FIXTURE_DIRECTORY.rglob("*"))

    assert main([str(FIXTURE_DIRECTORY), "--dry-run"]) == 0

    capsys.readouterr()
    after = sorted(path.relative_to(FIXTURE_DIRECTORY) for path in FIXTURE_DIRECTORY.rglob("*"))
    assert after == before


def test_execute_moves_logs_and_validates_disposable_fixture(tmp_path, monkeypatch):
    source = tmp_path / "scan"
    source.mkdir()
    (source / "notes.txt").write_text("notes", encoding="utf-8")
    (source / "README").write_text("unknown", encoding="utf-8")
    monkeypatch.setattr("scripts.file_organizer.FIXTURES_ROOT", tmp_path.resolve())
    files = classify_scanned_files(scan_fixture_directory(source))
    planned = plan_moves(files, load_schema(), source)

    log_path = source / "move_log.txt"
    log_lines = execute_moves(planned, log_path)
    validate_moves(planned)

    assert log_lines == [
        "MOVE notes.txt -> Documents\\notes.txt",
        "MOVE README -> unsorted\\README",
    ]
    assert log_path.read_text(encoding="utf-8") == "\n".join(log_lines) + "\n"


def test_main_execute_runs_only_against_disposable_fixture(tmp_path, capsys, monkeypatch):
    source = tmp_path / "scan"
    source.mkdir()
    (source / "song.mp3").write_text("audio", encoding="utf-8")
    monkeypatch.setattr("scripts.file_organizer.FIXTURES_ROOT", tmp_path.resolve())

    assert main([str(source), "--execute", "--confirm", "I APPROVE FILE MOVES"]) == 0

    assert "VALIDATED post-move layout" in capsys.readouterr().out
    assert (source / "Audio" / "song.mp3").is_file()
    assert (source / "move_log.txt").is_file()


def test_main_execute_requires_explicit_confirmation(tmp_path, capsys, monkeypatch):
    source = tmp_path / "scan"
    source.mkdir()
    (source / "song.mp3").write_text("audio", encoding="utf-8")
    monkeypatch.setattr("scripts.file_organizer.FIXTURES_ROOT", tmp_path.resolve())

    assert main([str(source), "--execute"]) == 2
    assert "Move blocked: pass --confirm \"I APPROVE FILE MOVES\"." in capsys.readouterr().out
    assert (source / "song.mp3").exists()
    assert not (source / "Audio").exists()

    assert main([str(source), "--execute", "--confirm", "I APPROVE FILE MOVES"]) == 0
    assert (source / "Audio" / "song.mp3").is_file()
