"""TaskHub UI target catalog used by Screenplay tasks and questions."""

from __future__ import annotations

from screenplay_core.core.target import Target


def _task_row_by_title_locator(page, title: str):
    return (
        page.locator('[data-testid="task-item"]')
        .filter(has=page.locator('[data-testid="task-title-text"]', has_text=title))
        .first
    )


class TaskHubTargets:
    LOGIN_USERNAME_INPUT = Target(
        "TaskHub login username input",
        lambda page: page.locator('[data-testid="login-username-input"]'),
    )
    LOGIN_PASSWORD_INPUT = Target(
        "TaskHub login password input",
        lambda page: page.locator('[data-testid="login-password-input"]'),
    )
    LOGIN_SUBMIT_BUTTON = Target(
        "TaskHub login submit button",
        lambda page: page.locator('[data-testid="login-submit-button"]'),
    )
    LOGIN_ERROR_MESSAGE = Target(
        "TaskHub login error message",
        lambda page: page.locator('[data-testid="login-error-message"]'),
    )

    FLASH_MESSAGE_CONTAINER = Target(
        "TaskHub flash message container",
        lambda page: page.locator('[data-testid="flash-message-container"]'),
    )

    TASK_LIST_CONTAINER = Target(
        "TaskHub task list container",
        lambda page: page.locator('[data-testid="task-list-container"]'),
    )
    TASK_TITLE_INPUT = Target(
        "TaskHub task title input",
        lambda page: page.locator('[data-testid="task-title-input"]'),
    )
    TASK_DESCRIPTION_INPUT = Target(
        "TaskHub task description input",
        lambda page: page.locator('[data-testid="task-description-input"]'),
    )
    TASK_PRIORITY_INPUT = Target(
        "TaskHub task priority input",
        lambda page: page.locator('[data-testid="task-priority-input"]'),
    )
    TASK_DUE_DATE_INPUT = Target(
        "TaskHub task due date input",
        lambda page: page.locator('[data-testid="task-due-date-input"]'),
    )
    ADD_TASK_BUTTON = Target(
        "TaskHub add task button",
        lambda page: page.locator('[data-testid="add-task-button"]'),
    )

    @classmethod
    def filter_button(cls, filter_name: str) -> Target:
        normalized = filter_name.strip().lower()
        return Target(
            f"TaskHub filter button {normalized}",
            lambda page: page.locator(f'[data-testid="filter-button"][data-filter="{normalized}"]'),
        )

    @classmethod
    def task_item_for_title(cls, title: str) -> Target:
        return Target(
            f"TaskHub task row for title '{title}'",
            lambda page: _task_row_by_title_locator(page, title),
        )

    @classmethod
    def edit_button_for_title(cls, title: str) -> Target:
        return Target(
            f"TaskHub edit button for title '{title}'",
            lambda page: _task_row_by_title_locator(page, title).locator(
                '[data-testid="edit-button"]'
            ),
        )

    @classmethod
    def delete_button_for_title(cls, title: str) -> Target:
        return Target(
            f"TaskHub delete button for title '{title}'",
            lambda page: _task_row_by_title_locator(page, title).locator(
                '[data-testid="delete-button"]'
            ),
        )

    @classmethod
    def complete_toggle_for_title(cls, title: str) -> Target:
        return Target(
            f"TaskHub complete toggle for title '{title}'",
            lambda page: _task_row_by_title_locator(page, title).locator(
                '[data-testid="complete-toggle"]'
            ),
        )

    @classmethod
    def edit_title_input_for_title(cls, title: str) -> Target:
        return Target(
            f"TaskHub edit title input for title '{title}'",
            lambda page: _task_row_by_title_locator(page, title).locator(
                '.edit-form input[name="title"]'
            ),
        )

    @classmethod
    def edit_description_input_for_title(cls, title: str) -> Target:
        return Target(
            f"TaskHub edit description input for title '{title}'",
            lambda page: _task_row_by_title_locator(page, title).locator(
                '.edit-form textarea[name="description"]'
            ),
        )

    @classmethod
    def edit_priority_input_for_title(cls, title: str) -> Target:
        return Target(
            f"TaskHub edit priority input for title '{title}'",
            lambda page: _task_row_by_title_locator(page, title).locator(
                '.edit-form select[name="priority"]'
            ),
        )

    @classmethod
    def edit_due_date_input_for_title(cls, title: str) -> Target:
        return Target(
            f"TaskHub edit due date input for title '{title}'",
            lambda page: _task_row_by_title_locator(page, title).locator(
                '.edit-form input[name="due_date"]'
            ),
        )

    @classmethod
    def save_button_for_title(cls, title: str) -> Target:
        return Target(
            f"TaskHub save button for title '{title}'",
            lambda page: _task_row_by_title_locator(page, title).locator(
                '[data-testid="save-button"]'
            ),
        )
