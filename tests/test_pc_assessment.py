import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from scripts.system.pc_assessment import CONFIRMATION_PHRASE, main
from scripts.system.pc_collectors import CollectionResult, POWERSHELL_COMMANDS, run_category
from scripts.system.pc_report import redact, redact_text, render_report, write_report


FIXTURES = Path(__file__).parent / "fixtures" / "pc_assessment"


def completed(stdout: str = "{}", stderr: str = "", returncode: int = 0):
    return subprocess.CompletedProcess([], returncode, stdout, stderr)


def test_run_category_uses_exact_allowlisted_command_without_shell():
    calls = []

    def executor(command, **kwargs):
        calls.append((command, kwargs))
        return completed((FIXTURES / "system.json").read_text(encoding="utf-8"))

    result = run_category("system", executor=executor)

    assert result.status == "collected"
    assert result.data["Caption"] == "Synthetic Windows"
    command, kwargs = calls[0]
    assert command[-1] == POWERSHELL_COMMANDS["system"]
    assert kwargs["shell"] is False
    assert kwargs["timeout"] == 30


def test_run_category_rejects_commands_outside_allowlist():
    with pytest.raises(ValueError, match="Unsupported assessment category"):
        run_category("Remove-Item C:\\")


def test_run_category_marks_access_denied_without_exposing_stderr():
    def executor(command, **kwargs):
        return completed(stderr="Access is denied: synthetic path", returncode=1)

    result = run_category("storage", executor=executor)

    assert result.status == "denied"
    assert result.error == "command"
    assert "synthetic path" not in repr(result)


def test_run_category_marks_malformed_output_as_failed():
    result = run_category("network", executor=lambda command, **kwargs: completed("not json"))

    assert result.status == "failed"
    assert result.error == "invalid_json"


def test_run_category_marks_timeout_and_missing_powershell():
    def timeout_executor(command, **kwargs):
        raise subprocess.TimeoutExpired(command, kwargs["timeout"])

    def missing_executor(command, **kwargs):
        raise FileNotFoundError("synthetic missing executable")

    assert run_category("drivers", executor=timeout_executor).error == "timeout"
    assert run_category("drivers", executor=missing_executor).status == "unavailable"


def test_allowlist_has_no_file_content_or_mutation_commands():
    blocked_terms = (
        "Get-ChildItem",
        "Get-Content",
        "Remove-Item",
        "Move-Item",
        "Set-ItemProperty",
        "Invoke-WebRequest",
    )

    assert not any(term in command for command in POWERSHELL_COMMANDS.values() for term in blocked_terms)
    assert all("OneDrive" not in command for command in POWERSHELL_COMMANDS.values())


def test_allowlist_covers_approved_assessment_scope():
    assert set(POWERSHELL_COMMANDS) == {
        "system",
        "updates",
        "security",
        "drivers",
        "hardware",
        "storage",
        "network",
        "software",
        "startup",
        "developer",
        "reliability",
    }


def test_fixture_contains_only_synthetic_values():
    data = json.loads((FIXTURES / "system.json").read_text(encoding="utf-8"))

    assert data["Caption"] == "Synthetic Windows"


def test_preview_is_default_and_executes_no_collectors(capsys):
    def forbidden_collector(category):
        raise AssertionError(f"preview executed {category}")

    assert main([], collector=forbidden_collector) == 0

    output = capsys.readouterr().out
    assert "no commands executed" in output
    assert "OneDrive" in output
    assert "file contents and directory traversal" in output
    assert "%LOCALAPPDATA%" not in output


def test_collection_requires_category_and_exact_confirmation(capsys):
    calls = []

    def collector(category):
        calls.append(category)
        return None

    assert main(["--collect"], collector=collector) == 2
    assert main(["--collect", "--category", "system"], collector=collector) == 2
    assert calls == []
    assert "Collection blocked" in capsys.readouterr().out


def test_approved_collection_reports_status_without_data(capsys):
    reports = []

    def collector(category):
        return run_category(
            category,
            executor=lambda command, **kwargs: completed('{"secret":"not printed"}'),
        )

    def report_writer(results):
        reports.extend(results)
        return Path("synthetic-report.md")

    assert main(
        [
            "--collect",
            "--category",
            "system",
            "--confirm",
            CONFIRMATION_PHRASE,
        ],
        collector=collector,
        report_writer=report_writer,
    ) == 0

    output = capsys.readouterr().out
    assert output == "system: collected\nRedacted report: synthetic-report.md\n"
    assert "not printed" not in output
    assert reports[0].status == "collected"


def test_report_redacts_paths_addresses_and_machine_identifiers(monkeypatch):
    monkeypatch.setattr("scripts.system.pc_report.socket.gethostname", lambda: "SYNTHETIC-HOST")
    value = "C:\\Users\\SyntheticUser\\secret.txt 192.168.10.2 AA-BB-CC-DD-EE-FF SYNTHETIC-HOST"

    redacted = redact_text(value)

    assert "secret.txt" not in redacted
    assert "192.168.10.2" not in redacted
    assert "AA-BB-CC-DD-EE-FF" not in redacted
    assert "SYNTHETIC-HOST" not in redacted


def test_report_redacts_sensitive_structured_fields():
    redacted = redact(
        {
            "User": "other-account",
            "SerialNumber": "SERIAL-123",
            "DisplayName": "Synthetic App",
        }
    )

    assert redacted == {
        "User": "<REDACTED>",
        "SerialNumber": "<REDACTED>",
        "DisplayName": "Synthetic App",
    }


def test_report_ranks_failed_collection_before_collected():
    report = render_report(
        [
            CollectionResult("system", "collected", {"Caption": "Synthetic Windows"}),
            CollectionResult("network", "failed", error="command"),
        ],
        generated_at=datetime(2026, 9, 16, tzinfo=timezone.utc),
    )

    assert report.index("network: failed") < report.index("system: collected")
    assert "## Window and scope" in report
    assert "## Executive assessment" in report
    assert "## Predictions" in report
    assert "## Suggested actions" in report
    assert "## Data and uncertainty" in report
    assert "No update, uninstall" in report


def test_report_flags_security_driver_and_storage_findings():
    report = render_report(
        [
            CollectionResult(
                "security",
                "collected",
                {
                    "Defender": {"RealTimeProtectionEnabled": False},
                    "FirewallProfiles": [{"Name": "Public", "Enabled": False}],
                },
            ),
            CollectionResult(
                "drivers",
                "collected",
                {"SignedDrivers": [], "ProblemDevices": [{"FriendlyName": "Synthetic device"}]},
            ),
            CollectionResult(
                "storage",
                "collected",
                {"Volumes": [{"DriveLetter": "X", "Size": 1000, "SizeRemaining": 50}]},
            ),
        ],
        generated_at=datetime(2026, 9, 16, tzinfo=timezone.utc),
    )

    assert "disabled protections" in report
    assert "disabled firewall profiles" in report
    assert "non-OK state" in report
    assert "X has 5.0% free space" in report


def test_report_summarizes_reliability_event_groups():
    report = render_report(
        [
            CollectionResult(
                "reliability",
                "collected",
                {
                    "SystemWarningAndErrorGroups": [
                        {"Count": 3, "Name": "SyntheticProvider, 100"},
                        {"Count": 2, "Name": "SyntheticProvider, 200"},
                    ]
                },
            )
        ],
        generated_at=datetime(2026, 9, 16, tzinfo=timezone.utc),
    )

    assert "5 warning/error event(s) across 2 top group(s)" in report


def test_report_flags_hardware_stability_signals():
    report = render_report(
        [
            CollectionResult(
                "hardware",
                "collected",
                {
                    "ProblemDevices": [{"FriendlyName": "Synthetic device"}],
                    "WHEA": [{"Id": 18}],
                },
            )
        ],
        generated_at=datetime(2026, 9, 16, tzinfo=timezone.utc),
    )

    assert "hardware: 1 present device(s) reported a non-OK state" in report
    assert "hardware: 1 WHEA hardware event(s)" in report


def test_write_report_uses_explicit_test_destination(tmp_path):
    output = write_report(
        [CollectionResult("system", "collected", {"Caption": "Synthetic Windows"})],
        destination=tmp_path,
        generated_at=datetime(2026, 9, 16, 12, 30, tzinfo=timezone.utc),
    )

    assert output == tmp_path / "pc-assessment-20260916-123000.md"
    assert "Synthetic Windows" in output.read_text(encoding="utf-8")
