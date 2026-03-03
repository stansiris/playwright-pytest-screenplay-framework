import os
from dataclasses import dataclass

DEFAULT_BASE_URL = "https://www.saucedemo.com/"
VALID_BROWSERS = {"chromium", "firefox", "webkit"}
TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default

    value = raw.strip().lower()
    if value in TRUE_VALUES:
        return True
    if value in FALSE_VALUES:
        return False

    raise ValueError(
        f"Invalid boolean value for {name}: '{raw}'. "
        "Use one of: 1, 0, true, false, yes, no, on, off."
    )


def _env_int(name: str, default: int, minimum: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default

    try:
        value = int(raw.strip())
    except ValueError as exc:
        raise ValueError(f"Invalid integer value for {name}: '{raw}'.") from exc

    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}. Got {value}.")

    return value


def _env_base_url() -> str:
    base_url = (os.getenv("BASE_URL") or DEFAULT_BASE_URL).strip() or DEFAULT_BASE_URL
    if not base_url.startswith(("http://", "https://")):
        raise ValueError("BASE_URL must start with http:// or https://.")
    if not base_url.endswith("/"):
        base_url = f"{base_url}/"
    return base_url


@dataclass(frozen=True, slots=True)
class RuntimeSettings:
    base_url: str
    browser: str
    headed: bool
    slow_mo_ms: int
    default_timeout_ms: int


def load_runtime_settings() -> RuntimeSettings:
    browser = (os.getenv("BROWSER") or "chromium").strip().lower()
    if browser not in VALID_BROWSERS:
        supported = ", ".join(sorted(VALID_BROWSERS))
        raise ValueError(f"Unsupported BROWSER '{browser}'. Supported values: {supported}.")

    timeout_env_name = (
        "SCREENPLAY_DEFAULT_TIMEOUT_MS"
        if os.getenv("SCREENPLAY_DEFAULT_TIMEOUT_MS") is not None
        else "DEFAULT_TIMEOUT_MS"
    )

    return RuntimeSettings(
        base_url=_env_base_url(),
        browser=browser,
        headed=_env_bool("HEADED", default=False),
        slow_mo_ms=_env_int("SLOW_MO_MS", default=0, minimum=0),
        default_timeout_ms=_env_int(timeout_env_name, default=5000, minimum=1),
    )


runtime_settings = load_runtime_settings()
