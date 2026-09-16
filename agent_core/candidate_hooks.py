"""Opt-in candidate lifecycle hook execution."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import math
from typing import Any, Callable, Mapping


Hook = Callable[..., Any]


class CandidateHookRunner:
    def __init__(
        self,
        config: Mapping[str, Any] | None,
        introspector: Any,
        registry: Mapping[str, Hook] | None,
    ) -> None:
        self.config = deepcopy(config or {})
        self.introspector = introspector
        self.registry = dict(registry or {})

    def _hooks_config(self) -> Mapping[str, Any]:
        hooks = self.config.get("hooks", {})
        return hooks if isinstance(hooks, Mapping) else {}

    def _emit_event(
        self,
        *,
        event: str,
        hook_type: str,
        hook_name: str,
        order_index: int,
        input_candidate: Any,
        output_candidate: Any,
        input_score: Any,
        output_score: Any,
        dry_run: bool,
        error: str | None,
    ) -> None:
        payload = {
            "event": event,
            "hook_type": hook_type,
            "hook_name": hook_name,
            "input_candidate": deepcopy(input_candidate),
            "output_candidate": deepcopy(output_candidate),
            "input_score": input_score,
            "output_score": output_score,
            "dry_run": dry_run,
            "error": error,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "order_index": order_index,
        }
        self.introspector.record(payload)

    @staticmethod
    def _dry_run(context: Mapping[str, Any]) -> bool:
        return context.get("dry_run", False) is True

    def run_pre_hooks(self, candidate: Mapping[str, Any], context: Mapping[str, Any]) -> Any:
        hooks = self._hooks_config()
        if hooks.get("enabled", False) is not True:
            return candidate

        current = candidate
        dry_run = self._dry_run(context)
        order_index = 0
        for entry in hooks.get("pre", []):
            if entry.get("enabled", False) is not True:
                continue
            name = entry.get("name")
            input_candidate = deepcopy(current)
            output_candidate = deepcopy(input_candidate)
            error = None
            hook = self.registry.get(name)
            event = "hook_called"

            if hook is None:
                error = "hook_not_found"
                event = "hook_error"
            else:
                try:
                    result = hook(deepcopy(input_candidate), context)
                    if dry_run:
                        event = "hook_skipped_due_to_dry_run"
                    elif result is not None:
                        output_candidate = deepcopy(result)
                except Exception as exc:  # Hook failures must not escape.
                    error = str(exc)
                    event = "hook_error"

            self._emit_event(
                event=event,
                hook_type="pre",
                hook_name=name,
                order_index=order_index,
                input_candidate=input_candidate,
                output_candidate=(
                    input_candidate if dry_run and error is None else output_candidate
                ),
                input_score=None,
                output_score=None,
                dry_run=dry_run,
                error=error,
            )
            if not dry_run and error is None and hook is not None:
                current = output_candidate
            order_index += 1
        return current

    def run_post_hooks(
        self,
        candidate: Mapping[str, Any],
        score: float,
        context: Mapping[str, Any],
    ) -> tuple[Any, float]:
        hooks = self._hooks_config()
        if hooks.get("enabled", False) is not True:
            return candidate, score

        current_candidate = candidate
        current_score = score
        dry_run = self._dry_run(context)
        order_index = 0
        for entry in hooks.get("post", []):
            if entry.get("enabled", False) is not True:
                continue
            name = entry.get("name")
            input_candidate = deepcopy(current_candidate)
            input_score = current_score
            output_candidate = deepcopy(input_candidate)
            output_score = input_score
            error = None
            hook = self.registry.get(name)
            event = "hook_called"

            if hook is None:
                error = "hook_not_found"
                event = "hook_error"
            else:
                try:
                    result = hook(deepcopy(input_candidate), input_score, context)
                    if dry_run:
                        event = "hook_skipped_due_to_dry_run"
                    elif result is not None:
                        candidate_out, score_out = result
                        if not isinstance(score_out, (int, float)) or isinstance(
                            score_out, bool
                        ) or not math.isfinite(score_out) or not 0 <= score_out <= 1:
                            error = "invalid_score"
                            event = "hook_error"
                        else:
                            output_candidate = deepcopy(candidate_out)
                            output_score = float(score_out)
                except Exception as exc:  # Hook failures must not escape.
                    error = str(exc)
                    event = "hook_error"

            self._emit_event(
                event=event,
                hook_type="post",
                hook_name=name,
                order_index=order_index,
                input_candidate=input_candidate,
                output_candidate=(
                    input_candidate if dry_run and error is None else output_candidate
                ),
                input_score=input_score,
                output_score=(
                    input_score if dry_run and error is None else output_score
                ),
                dry_run=dry_run,
                error=error,
            )
            if not dry_run and error is None and hook is not None:
                current_candidate = output_candidate
                current_score = output_score
            order_index += 1
        return current_candidate, current_score
