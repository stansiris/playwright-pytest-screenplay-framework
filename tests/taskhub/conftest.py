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

from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.abilities.call_the_api import CallTheAPI
from screenplay_core.consequences.ensure import Ensure
from screenplay_core.core.actor import Actor
from taskhub.automation.tasks.login import LoginToTaskHub
from taskhub.automation.tasks.open_taskhub import OpenTaskHub
from taskhub.automation.ui.targets import TaskHubTargets

REPO_ROOT = Path(__file__).resolve().parents[2]


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def _wait_until_healthy(base_url: str, timeout_seconds: float = 20.0) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
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

    environment = os.environ.copy()
    environment["TASKHUB_PORT"] = str(port)
    environment["TASKHUB_DB_PATH"] = str(db_path)
    environment["TASKHUB_SECRET_KEY"] = "taskhub-test-secret"

    process = subprocess.Popen(
        [sys.executable, "-m", "taskhub.app.app"],
        cwd=str(REPO_ROOT),
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base_url = f"http://127.0.0.1:{port}"

    try:
        _wait_until_healthy(base_url)
    except Exception as exc:
        process.terminate()
        raise RuntimeError("Failed to start TaskHub server.") from exc

    yield {"base_url": base_url, "db_path": str(db_path), "port": port}

    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=10)


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
    actor = Actor("TaskHub API Client").can(CallTheAPI.at(taskhub_base_url.rstrip("/")))
    yield actor
    actor.ability_to(CallTheAPI).close()
