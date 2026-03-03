class BrowseTheWeb:
    """
    Ability wrapper around Playwright's page.
    Keeps Playwright details out of Actor/Tasks.
    """

    def __init__(
        self,
        page,
        base_url: str | None = None,
        default_timeout_ms: int = 5000,
    ):
        if default_timeout_ms < 1:
            raise ValueError("default_timeout_ms must be >= 1.")
        self.page = page
        self.base_url = base_url
        self.default_timeout_ms = default_timeout_ms

    @staticmethod
    def using(
        page,
        base_url: str | None = None,
        default_timeout_ms: int = 5000,
    ):
        return BrowseTheWeb(page, base_url, default_timeout_ms)
