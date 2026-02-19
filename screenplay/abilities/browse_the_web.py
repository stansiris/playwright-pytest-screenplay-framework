class BrowseTheWeb:
    """
    Ability wrapper around Playwright's page.
    Keeps Playwright details out of Actor/Tasks.
    """

    def __init__(self, page):
        self.page = page

    @staticmethod
    def using(page):
        return BrowseTheWeb(page)
