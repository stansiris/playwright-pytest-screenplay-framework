class BrowseTheWeb:
    """
    Ability wrapper around Playwright's page.
    Keeps Playwright details out of Actor/Tasks.
    """

    def __init__(self, page, base_url: str | None = None):
        self.page = page
        self.base_url = base_url

    @staticmethod
    def using(page, base_url: str | None = None):
        return BrowseTheWeb(page, base_url)
