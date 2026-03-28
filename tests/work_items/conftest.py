"""Shared Work Items fixtures for server lifecycle, actors, and data reset."""

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

from examples.work_items.automation.tasks.login import LoginToWorkItems
from examples.work_items.automation.tasks.open_work_items import OpenWorkItems
from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.actor import Actor
from screenplay_core.http.call_the_api import CallTheApi
from screenplay_core.playwright.browse_the_web import BrowseTheWeb
from screenplay_core.playwright.ensure import Ensure

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
                f"Work Items server process exited early with code {process.returncode}."
            )
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                return
        except requests.RequestException:
            time.sleep(0.2)
            continue
        time.sleep(0.2)
    raise RuntimeError("Work Items server did not become healthy in time.")


@pytest.fixture(scope="session")
def work_items_server(tmp_path_factory):
    port = _find_free_port()
    db_path = tmp_path_factory.mktemp("work-items-data") / "work_items.db"
    log_path = tmp_path_factory.mktemp("work-items-logs") / f"work-items-server-{port}.stderr.log"

    environment = os.environ.copy()
    environment["WORK_ITEMS_PORT"] = str(port)
    environment["WORK_ITEMS_DB_PATH"] = str(db_path)
    environment["WORK_ITEMS_SECRET_KEY"] = "work-items-test-secret"

    stderr_handle = log_path.open(mode="w", encoding="utf-8")
    process = subprocess.Popen(
        [sys.executable, "-m", "examples.work_items.app.app"],
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
        message = f"Failed to start Work Items server. stderr log: {log_path}"
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
def work_items_base_url(work_items_server) -> str:
    return work_items_server["base_url"].rstrip("/") + "/"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, work_items_server) -> dict:
    """Inject the dynamic Work Items base_url into every BrowserContext for this suite."""
    return {**browser_context_args, "base_url": work_items_server["base_url"]}


@pytest.fixture(autouse=True)
def reset_work_items_data(work_items_base_url: str) -> None:
    response = requests.post(f"{work_items_base_url.rstrip('/')}/api/test/reset", timeout=10)
    response.raise_for_status()


@pytest.fixture
def work_items_customer(page, work_items_base_url: str) -> Actor:
    return Actor("Work Items Customer").can(BrowseTheWeb.using(page, base_url=work_items_base_url))


@pytest.fixture
def work_items_logged_in_customer(work_items_customer: Actor) -> Actor:
    work_items_customer.attempts_to(
        OpenWorkItems.app(),
        Ensure.that(WorkItemsTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToWorkItems.with_credentials("admin", "admin123"),
        Ensure.that(WorkItemsTargets.WORK_ITEM_LIST_CONTAINER).to_be_visible(),
    )
    return work_items_customer


@pytest.fixture
def work_items_api_actor(work_items_base_url: str) -> Iterator[Actor]:
    actor = Actor("Work Items API Actor").can(CallTheApi.at(work_items_base_url.rstrip("/")))
    yield actor
    actor.ability_to(CallTheApi).close()
