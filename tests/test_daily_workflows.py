import json
from pathlib import Path

import pytest

from scripts import daily_briefing
from scripts.daily_briefing import write_atomic
from scripts.system.tuning_record import append_record
from scripts.voice_file_organizer import directory_from_transcript, main as voice_main


def test_voice_command_extracts_explicit_fixture_directory():
    assert directory_from_transcript('Organize files in "tests/fixtures/inbox"') == Path(
        "tests/fixtures/inbox"
    )


def test_voice_command_rejects_ambiguous_transcript():
    with pytest.raises(ValueError, match="organize files in"):
        directory_from_transcript("move everything")


def test_voice_command_only_runs_dry_run(capsys):
    fixture = Path(__file__).parent / "fixtures" / "file_organizer_scan"

    assert voice_main([f"organize files in {fixture}"]) == 0

    assert "notes.txt ->" in capsys.readouterr().out
    assert (fixture / "notes.txt").is_file()


def test_tuning_record_requires_complete_rollback_metadata(tmp_path):
    with pytest.raises(ValueError, match="evidence"):
        append_record(
            tmp_path / "tuning.jsonl",
            setting="memory profile",
            before="default",
            after="profile",
            rollback="restore default",
            evidence="",
        )


def test_tuning_record_is_structured_and_non_mutating(tmp_path):
    output = tmp_path / "tuning.jsonl"
    append_record(
        output,
        setting="memory profile",
        before="default",
        after="profile",
        rollback="restore default",
        evidence="baseline report",
    )

    record = json.loads(output.read_text(encoding="utf-8"))
    assert record["setting"] == "memory profile"
    assert record["rollback"] == "restore default"


def test_briefing_write_is_atomic(tmp_path):
    output = tmp_path / "briefing.md"
    write_atomic(output, "complete report\n")

    assert output.read_text(encoding="utf-8") == "complete report\n"
    assert not output.with_name(".briefing.md.tmp").exists()


def test_briefing_ignores_generated_and_vendored_files(tmp_path, monkeypatch):
    source = tmp_path / "scripts" / "worker.py"
    cache = tmp_path / ".pytest_cache" / "state.json"
    environment = tmp_path / ".venv" / "Lib" / "dependency.py"
    dependency = tmp_path / "forgecheck" / "dependencies" / "package.py"
    for path in (source, cache, environment, dependency):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("content", encoding="utf-8")
    monkeypatch.setattr(daily_briefing, "ROOT", tmp_path)

    assert daily_briefing.workspace_files() == [source]
    assert daily_briefing.count_files(".py") == 1
