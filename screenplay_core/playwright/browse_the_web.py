class BrowseTheWeb:
    """
    Ability wrapper around Playwright's page.
    Keeps Playwright details out of Actor/Tasks.
    """

    def __init__(
        self,
        page,
        base_url: str | None = None,
    ):
        """Store browser page context and optional base URL for navigation tasks."""
        self.page = page
        self.base_url = base_url

    @staticmethod
    def using(
        page,
        base_url: str | None = None,
    ) -> "BrowseTheWeb":
        """Factory for readability in actor fixture setup."""
        return BrowseTheWeb(page, base_url)
