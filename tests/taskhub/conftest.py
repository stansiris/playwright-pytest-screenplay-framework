"""Shared TaskHub fixtures for server lifecycle, actors, and data reset."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from collections.abc import Iterator
from pathlib import Path

import pytest
import requests

from examples.taskhub.automation.tasks.login import LoginToTaskHub
from examples.taskhub.automation.tasks.open_taskhub import OpenTaskHub
from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.abilities.call_the_api import CallTheApi
from screenplay_core.consequences.ensure import Ensure
from screenplay_core.core.actor import Actor

REPO_ROOT = Path(__file__).resolve().parents[2]


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def _read_log_excerpt(log_path: Path, max_lines: int = 80) -> str:
    if not log_path.exists():
        return ""

    raw_text = log_path.read_text(encoding="utf-8", errors="replace")
    lines = raw_text.splitlines()
    if not lines:
        return ""

    excerpt_lines = lines[-max_lines:]
    return "\n".join(excerpt_lines)


def _wait_until_healthy(
    base_url: str,
    process: subprocess.Popen | None = None,
    timeout_seconds: float = 20.0,
) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if process is not None and process.poll() is not None:
            raise RuntimeError(
                f"TaskHub server process exited early with code {process.returncode}."
            )
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                return
        except requests.RequestException:
            time.sleep(0.2)
            continue
        time.sleep(0.2)
    raise RuntimeError("TaskHub server did not become healthy in time.")


@pytest.fixture(scope="session")
def taskhub_server(tmp_path_factory):
    port = _find_free_port()
    db_path = tmp_path_factory.mktemp("taskhub-data") / "taskhub.db"
    log_path = tmp_path_factory.mktemp("taskhub-logs") / f"taskhub-server-{port}.stderr.log"

    environment = os.environ.copy()
    environment["TASKHUB_PORT"] = str(port)
    environment["TASKHUB_DB_PATH"] = str(db_path)
    environment["TASKHUB_SECRET_KEY"] = "taskhub-test-secret"

    stderr_handle = log_path.open(mode="w", encoding="utf-8")
    process = subprocess.Popen(
        [sys.executable, "-m", "examples.taskhub.app.app"],
        cwd=str(REPO_ROOT),
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=stderr_handle,
    )
    base_url = f"http://127.0.0.1:{port}"

    try:
        _wait_until_healthy(base_url, process=process)
    except Exception as exc:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

        stderr_handle.flush()
        stderr_handle.close()
        log_excerpt = _read_log_excerpt(log_path)
        message = f"Failed to start TaskHub server. stderr log: {log_path}"
        if log_excerpt:
            message = f"{message}\n--- stderr tail ---\n{log_excerpt}"
        else:
            message = f"{message}\n(no stderr output captured)"
        raise RuntimeError(message) from exc

    yield {
        "base_url": base_url,
        "db_path": str(db_path),
        "port": port,
        "stderr_log_path": str(log_path),
    }

    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=10)
    finally:
        stderr_handle.close()


@pytest.fixture(scope="session")
def taskhub_base_url(taskhub_server) -> str:
    return taskhub_server["base_url"].rstrip("/") + "/"


@pytest.fixture(autouse=True)
def reset_taskhub_data(taskhub_base_url: str) -> None:
    response = requests.post(f"{taskhub_base_url.rstrip('/')}/api/test/reset", timeout=10)
    response.raise_for_status()


@pytest.fixture
def taskhub_customer(page, taskhub_base_url: str) -> Actor:
    return Actor("TaskHub Customer").can(BrowseTheWeb.using(page, base_url=taskhub_base_url))


@pytest.fixture
def taskhub_logged_in_customer(taskhub_customer: Actor) -> Actor:
    taskhub_customer.attempts_to(
        OpenTaskHub.app(),
        Ensure.that(TaskHubTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToTaskHub.with_credentials("admin", "admin123"),
        Ensure.that(TaskHubTargets.TASK_LIST_CONTAINER).to_be_visible(),
    )
    return taskhub_customer


@pytest.fixture
def taskhub_api_actor(taskhub_base_url: str) -> Iterator[Actor]:
    actor = Actor("TaskHub API Client").can(CallTheApi.at(taskhub_base_url.rstrip("/")))
    yield actor
    actor.ability_to(CallTheApi).close()
