"""Data schemas for documentation-driven test generation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class IntentStep:
    """Canonical step captured from user documentation."""

    action: str
    params: dict[str, Any] = field(default_factory=dict)
    source: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"action": self.action, "params": self.params}
        if self.source:
            payload["source"] = self.source
        return payload

    @staticmethod
    def from_dict(payload: dict[str, Any]) -> "IntentStep":
        if "action" not in payload:
            raise ValueError("IntentStep payload must include an 'action' field.")

        params = payload.get("params", {})
        if not isinstance(params, dict):
            raise ValueError("IntentStep 'params' must be a dictionary.")

        source = payload.get("source")
        if source is not None and not isinstance(source, str):
            raise ValueError("IntentStep 'source' must be a string when provided.")

        return IntentStep(action=str(payload["action"]), params=params, source=source)


@dataclass
class TestIntent:
    """Structured test intent used by mappers and generators."""

    name: str
    actor_name: str = "Customer"
    base_url: str = "https://www.saucedemo.com/"
    steps: list[IntentStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "actor_name": self.actor_name,
            "base_url": self.base_url,
            "steps": [step.to_dict() for step in self.steps],
            "metadata": self.metadata,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def write_json(self, output_path: str | Path, indent: int = 2) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_json(indent=indent), encoding="utf-8")
        return path

    @staticmethod
    def from_dict(payload: dict[str, Any]) -> "TestIntent":
        if "name" not in payload:
            raise ValueError("TestIntent payload must include a 'name' field.")

        raw_steps = payload.get("steps", [])
        if not isinstance(raw_steps, list):
            raise ValueError("TestIntent 'steps' must be a list.")

        steps = [IntentStep.from_dict(step) for step in raw_steps]

        metadata = payload.get("metadata", {})
        if not isinstance(metadata, dict):
            raise ValueError("TestIntent 'metadata' must be a dictionary.")

        return TestIntent(
            name=str(payload["name"]),
            actor_name=str(payload.get("actor_name", "Customer")),
            base_url=str(payload.get("base_url", "https://www.saucedemo.com/")),
            steps=steps,
            metadata=metadata,
        )

    @staticmethod
    def from_json(json_text: str) -> "TestIntent":
        return TestIntent.from_dict(json.loads(json_text))


def load_test_intent(input_path: str | Path) -> TestIntent:
    """Load a TestIntent JSON file from disk."""

    path = Path(input_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    return TestIntent.from_dict(payload)
