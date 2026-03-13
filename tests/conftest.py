import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig) -> dict:
    launch_options: dict[str, int | str | bool] = {}

    if pytestconfig.getoption("--headed"):
        launch_options["headless"] = False

    slowmo_cli = pytestconfig.getoption("--slowmo")
    if slowmo_cli is not None:
        launch_options["slow_mo"] = slowmo_cli

    browser_channel = pytestconfig.getoption("--browser-channel")
    if browser_channel:
        launch_options["channel"] = browser_channel

    return launch_options
