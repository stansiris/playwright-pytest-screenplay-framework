import os
from dataclasses import dataclass

DEFAULT_BASE_URL = "https://www.saucedemo.com/"
VALID_BROWSERS = {"chromium", "firefox", "webkit"}


def _parse_bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default

    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False

    raise ValueError(
        f"Invalid boolean value for {name}: '{raw}'. "
        "Use one of: 1, 0, true, false, yes, no, on, off."
    )


def _parse_int_env(name: str, default: int, minimum: int) -> int:
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


@dataclass(frozen=True)
class RuntimeSettings:
    base_url: str
    browser: str
    headed: bool
    slow_mo_ms: int
    default_timeout_ms: int

    @staticmethod
    def from_env() -> "RuntimeSettings":
        base_url = (os.getenv("BASE_URL") or DEFAULT_BASE_URL).strip() or DEFAULT_BASE_URL
        if not base_url.startswith(("http://", "https://")):
            raise ValueError("BASE_URL must start with http:// or https://.")
        if not base_url.endswith("/"):
            base_url = f"{base_url}/"

        browser = (os.getenv("BROWSER") or "chromium").strip().lower()
        if browser not in VALID_BROWSERS:
            supported = ", ".join(sorted(VALID_BROWSERS))
            raise ValueError(f"Unsupported BROWSER '{browser}'. Supported values: {supported}.")

        return RuntimeSettings(
            base_url=base_url,
            browser=browser,
            headed=_parse_bool_env("HEADED", default=False),
            slow_mo_ms=_parse_int_env("SLOW_MO_MS", default=0, minimum=0),
            default_timeout_ms=_parse_int_env("DEFAULT_TIMEOUT_MS", default=5000, minimum=1),
        )


runtime_settings = RuntimeSettings.from_env()
