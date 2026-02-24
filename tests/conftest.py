import pytest

from saucedemo.config.runtime import runtime_settings
from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor


def pytest_configure(config) -> None:
    if hasattr(config.option, "browser") and not config.option.browser:
        config.option.browser = [runtime_settings.browser]


@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    cli_base_url = pytestconfig.getoption("base_url")
    if cli_base_url:
        return cli_base_url.rstrip("/") + "/"
    return runtime_settings.base_url


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig) -> dict:
    launch_options: dict[str, int | str | bool] = {}

    if pytestconfig.getoption("--headed") or runtime_settings.headed:
        launch_options["headless"] = False

    slowmo_cli = pytestconfig.getoption("--slowmo")
    if slowmo_cli:
        launch_options["slow_mo"] = slowmo_cli
    elif runtime_settings.slow_mo_ms:
        launch_options["slow_mo"] = runtime_settings.slow_mo_ms

    browser_channel = pytestconfig.getoption("--browser-channel")
    if browser_channel:
        launch_options["channel"] = browser_channel

    return launch_options


@pytest.fixture
def customer(page):
    return Actor("Customer").can(BrowseTheWeb.using(page))
