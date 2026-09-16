import math

from verifier import choose_best_candidate, evaluate_candidate


def test_logs_candidate_acceptance(capfd):
    result = evaluate_candidate({"id": "accepted", "output": "ok", "score": 1.5})

    assert result.accepted is True
    out, err = capfd.readouterr()
    assert err == ""
    assert "candidate_accepted" in out
    assert '"candidate_id": "accepted"' in out


def test_logs_candidate_rejection(capfd):
    result = evaluate_candidate({"id": "missing", "score": 1})

    assert result.accepted is False
    out, err = capfd.readouterr()
    assert err == ""
    assert "candidate_rejected" in out
    assert "candidate_output_missing" in out


def test_logs_non_finite_score_rejection(capfd):
    result = evaluate_candidate(
        {"id": "non-finite", "output": "bad", "score": math.nan}
    )

    assert result.accepted is False
    out, err = capfd.readouterr()
    assert err == ""
    assert "score_rejected_non_finite" in out
    assert "candidate_rejected" in out


def test_logs_final_selection_without_changing_result(capfd):
    candidates = [
        {"id": "a", "output": "low", "score": 1.0},
        {"id": "b", "output": "high", "score": 2.0},
    ]

    selected = choose_best_candidate(candidates)

    assert selected == candidates[1]
    out, err = capfd.readouterr()
    assert err == ""
    assert "candidate_selected" in out
    assert '"candidate_id": "b"' in out


def test_logs_empty_selection_fallback(capfd):
    assert choose_best_candidate([]) is None

    out, err = capfd.readouterr()
    assert err == ""
    assert "candidate_selection_empty" in out
