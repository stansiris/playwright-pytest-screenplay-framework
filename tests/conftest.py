import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--maximized", action="store_true", default=False, help="Launch browser maximized."
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig) -> dict:
    launch_options: dict[str, int | str | bool | list] = {}

    if pytestconfig.getoption("--headed"):
        launch_options["headless"] = False

    slowmo_cli = pytestconfig.getoption("--slowmo")
    if slowmo_cli is not None:
        launch_options["slow_mo"] = slowmo_cli

    browser_channel = pytestconfig.getoption("--browser-channel")
    if browser_channel:
        launch_options["channel"] = browser_channel

    if pytestconfig.getoption("--maximized"):
        launch_options["args"] = ["--start-maximized"]

    return launch_options


@pytest.fixture(scope="session")
def browser_context_args(pytestconfig, browser_context_args: dict) -> dict:
    if pytestconfig.getoption("--maximized"):
        return {**browser_context_args, "no_viewport": True}
    return browser_context_args
