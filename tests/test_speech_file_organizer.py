from pathlib import Path

from scripts.speech_file_organizer import (
    main,
    run_dry_run_from_transcript,
    transcript_requests_dry_run,
    transcript_requests_execution,
)


def test_transcript_requests_dry_run_requires_organizer_preview_intent():
    assert transcript_requests_dry_run("please organize files dry run")
    assert transcript_requests_dry_run("preview file organization by sorting this folder")
    assert not transcript_requests_dry_run("organize files")
    assert not transcript_requests_dry_run("dry run the report")


def test_transcript_requests_execution_detects_real_move_intent():
    assert transcript_requests_execution("execute the organizer")
    assert transcript_requests_execution("move files now")
    assert transcript_requests_execution("I APPROVE FILE MOVES")
    assert not transcript_requests_execution("preview file organization")


def test_speech_transcript_triggers_file_organizer_dry_run(capsys):
    fixture_directory = Path(__file__).parent / "fixtures" / "file_organizer_scan"

    assert (
        run_dry_run_from_transcript("please organize files dry run", fixture_directory)
        == 0
    )

    assert capsys.readouterr().out.splitlines() == [
        "Transcript accepted for dry-run: please organize files dry run",
        "notes.txt -> Documents\\notes.txt",
        "photo.JPG -> Images\\photo.JPG",
        "README -> unsorted\\README",
        "song.MP3 -> Audio\\song.MP3",
    ]


def test_speech_transcript_cannot_execute_moves(tmp_path, capsys, monkeypatch):
    source = tmp_path / "scan"
    source.mkdir()
    (source / "song.mp3").write_text("audio", encoding="utf-8")
    monkeypatch.setattr("scripts.file_organizer.FIXTURES_ROOT", tmp_path.resolve())

    assert (
        run_dry_run_from_transcript("execute organize files I APPROVE FILE MOVES", source)
        == 2
    )

    output = capsys.readouterr().out
    assert "transcripts can only request dry-runs" in output
    assert (source / "song.mp3").is_file()
    assert not (source / "Audio").exists()
    assert not (source / "move_log.txt").exists()


def test_speech_cli_omits_execute_and_confirm_options(capsys):
    fixture_directory = Path(__file__).parent / "fixtures" / "file_organizer_scan"

    assert main([str(fixture_directory), "--transcript", "preview file organization"]) == 0

    output = capsys.readouterr().out
    assert "Transcript accepted for dry-run" in output
    assert "VALIDATED post-move layout" not in output
