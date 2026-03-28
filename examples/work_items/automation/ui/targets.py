"""Work Items UI target catalog used by Screenplay tasks and questions."""

from __future__ import annotations

import re

from screenplay_core.playwright.target import Target


def _work_item_card_by_id_locator(page, work_item_id: int):
    return page.locator(f'[data-testid="work-item-card"][data-work-item-id="{work_item_id}"]')


def _work_item_card_by_title_locator(page, title: str):
    exact_title_pattern = re.compile(rf"^{re.escape(title)}$")
    return (
        page.locator('[data-testid="work-item-card"]')
        .filter(
            has=page.locator('[data-testid="work-item-title-text"]', has_text=exact_title_pattern)
        )
        .first
    )


class WorkItemsTargets:
    LOGIN_USERNAME_INPUT = Target(
        "Work Items login username input",
        lambda page: page.locator('[data-testid="login-username-input"]'),
    )
    LOGIN_PASSWORD_INPUT = Target(
        "Work Items login password input",
        lambda page: page.locator('[data-testid="login-password-input"]'),
    )
    LOGIN_SUBMIT_BUTTON = Target(
        "Work Items login submit button",
        lambda page: page.locator('[data-testid="login-submit-button"]'),
    )
    LOGIN_ERROR_MESSAGE = Target(
        "Work Items login error message",
        lambda page: page.locator('[data-testid="login-error-message"]'),
    )
    FLASH_MESSAGE_CONTAINER = Target(
        "Work Items flash message container",
        lambda page: page.locator('[data-testid="flash-message-container"]'),
    )

    WORK_ITEM_LIST_CONTAINER = Target(
        "Work Items work item list container",
        lambda page: page.locator('[data-testid="work-item-list-container"]'),
    )
    WORK_ITEM_TITLE_INPUT = Target(
        "Work Items work item title input",
        lambda page: page.locator('[data-testid="work-item-title-input"]'),
    )
    WORK_ITEM_DESCRIPTION_INPUT = Target(
        "Work Items work item description input",
        lambda page: page.locator('[data-testid="work-item-description-input"]'),
    )
    WORK_ITEM_PRIORITY_INPUT = Target(
        "Work Items work item priority input",
        lambda page: page.locator('[data-testid="work-item-priority-input"]'),
    )
    WORK_ITEM_DUE_DATE_INPUT = Target(
        "Work Items work item due date input",
        lambda page: page.locator('[data-testid="work-item-due-date-input"]'),
    )
    ADD_WORK_ITEM_BUTTON = Target(
        "Work Items add work item button",
        lambda page: page.locator('[data-testid="add-work-item-button"]'),
    )
    LOGOUT_BUTTON = Target(
        "Work Items logout button",
        lambda page: page.locator('[data-testid="work-items-logout-button"]'),
    )

    @classmethod
    def filter_button(cls, filter_name: str) -> Target:
        normalized = filter_name.strip().lower()
        return Target(
            f"Work Items filter button {normalized}",
            lambda page: page.locator(f'[data-testid="filter-button"][data-filter="{normalized}"]'),
        )

    @classmethod
    def work_item_for_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items work item card for id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id),
        )

    @classmethod
    def work_item_for_title(cls, title: str) -> Target:
        return Target(
            f"Work Items work item card for title '{title}'",
            lambda page: _work_item_card_by_title_locator(page, title),
        )

    @classmethod
    def work_item_title_text_for_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items work item title text for id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id).locator(
                '[data-testid="work-item-title-text"]'
            ),
        )

    @classmethod
    def edit_button_for_work_item_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items edit button for work item id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id).locator(
                '[data-testid="edit-work-item-open-button"]'
            ),
        )

    @classmethod
    def delete_button_for_work_item_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items delete button for work item id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id).locator(
                '[data-testid="delete-work-item-button"]'
            ),
        )

    @classmethod
    def complete_toggle_for_work_item_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items completion toggle for work item id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id).locator(
                '[data-testid="work-item-completion-toggle"]'
            ),
        )

    @classmethod
    def edit_title_input_for_work_item_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items edit title input for work item id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id).locator(
                '[data-testid="edit-work-item-title-input"]'
            ),
        )

    @classmethod
    def edit_description_input_for_work_item_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items edit description input for work item id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id).locator(
                '[data-testid="edit-work-item-description-input"]'
            ),
        )

    @classmethod
    def edit_priority_input_for_work_item_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items edit priority input for work item id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id).locator(
                '[data-testid="edit-work-item-priority-select"]'
            ),
        )

    @classmethod
    def edit_due_date_input_for_work_item_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items edit due date input for work item id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id).locator(
                '[data-testid="edit-work-item-due-date-input"]'
            ),
        )

    @classmethod
    def save_button_for_work_item_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items save button for work item id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id).locator(
                '[data-testid="edit-work-item-save-button"]'
            ),
        )

    @classmethod
    def cancel_button_for_work_item_id(cls, work_item_id: int) -> Target:
        return Target(
            f"Work Items cancel button for work item id {work_item_id}",
            lambda page: _work_item_card_by_id_locator(page, work_item_id).locator(
                '[data-testid="edit-work-item-cancel-button"]'
            ),
        )

    @classmethod
    def edit_button_for_work_item_title(cls, title: str) -> Target:
        return Target(
            f"Work Items edit button for work item title '{title}'",
            lambda page: _work_item_card_by_title_locator(page, title).locator(
                '[data-testid="edit-work-item-open-button"]'
            ),
        )

    @classmethod
    def delete_button_for_work_item_title(cls, title: str) -> Target:
        return Target(
            f"Work Items delete button for work item title '{title}'",
            lambda page: _work_item_card_by_title_locator(page, title).locator(
                '[data-testid="delete-work-item-button"]'
            ),
        )

    @classmethod
    def complete_toggle_for_work_item_title(cls, title: str) -> Target:
        return Target(
            f"Work Items completion toggle for work item title '{title}'",
            lambda page: _work_item_card_by_title_locator(page, title).locator(
                '[data-testid="work-item-completion-toggle"]'
            ),
        )

    @classmethod
    def edit_title_input_for_work_item_title(cls, title: str) -> Target:
        return Target(
            f"Work Items edit title input for work item title '{title}'",
            lambda page: _work_item_card_by_title_locator(page, title).locator(
                '[data-testid="edit-work-item-title-input"]'
            ),
        )

    @classmethod
    def edit_description_input_for_work_item_title(cls, title: str) -> Target:
        return Target(
            f"Work Items edit description input for work item title '{title}'",
            lambda page: _work_item_card_by_title_locator(page, title).locator(
                '[data-testid="edit-work-item-description-input"]'
            ),
        )

    @classmethod
    def edit_priority_input_for_work_item_title(cls, title: str) -> Target:
        return Target(
            f"Work Items edit priority input for work item title '{title}'",
            lambda page: _work_item_card_by_title_locator(page, title).locator(
                '[data-testid="edit-work-item-priority-select"]'
            ),
        )

    @classmethod
    def edit_due_date_input_for_work_item_title(cls, title: str) -> Target:
        return Target(
            f"Work Items edit due date input for work item title '{title}'",
            lambda page: _work_item_card_by_title_locator(page, title).locator(
                '[data-testid="edit-work-item-due-date-input"]'
            ),
        )

    @classmethod
    def save_button_for_work_item_title(cls, title: str) -> Target:
        return Target(
            f"Work Items save button for work item title '{title}'",
            lambda page: _work_item_card_by_title_locator(page, title).locator(
                '[data-testid="edit-work-item-save-button"]'
            ),
        )
