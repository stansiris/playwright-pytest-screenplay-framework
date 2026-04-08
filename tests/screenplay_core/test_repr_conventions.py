from examples.work_items.automation.questions.api_questions import (
    FetchWorkItemViaApi,
    FetchWorkItemsViaApi,
    WorkItemExistsViaApi,
    WorkItemFieldEqualsViaApi,
    WorkItemIdForTitleViaApi,
)
from examples.work_items.automation.tasks.api_tasks import (
    CreateWorkItemViaApi,
    DeleteWorkItemViaApi,
    LoginToWorkItemsApi,
    UpdateWorkItemViaApi,
)
from screenplay_core.core.consequence import Consequence
from screenplay_core.core.interaction import Interaction
from screenplay_core.core.question import Question
from screenplay_core.core.task import Task


class MinimalQuestion(Question):
    def answered_by(self, actor):  # noqa: ANN001
        return None


class MinimalTask(Task):
    def perform_as(self, actor) -> None:  # noqa: ANN001
        return None


class MinimalInteraction(Interaction):
    def perform_as(self, actor) -> None:  # noqa: ANN001
        return None


class MinimalConsequence(Consequence):
    def perform_as(self, actor) -> None:  # noqa: ANN001
        return None


def test_question_base_repr_defaults_to_class_name() -> None:
    """Verify simple questions have a readable fallback representation."""
    assert repr(MinimalQuestion()) == "MinimalQuestion()"


def test_task_base_repr_defaults_to_class_name() -> None:
    """Verify simple tasks keep the inherited readable task representation."""
    assert repr(MinimalTask()) == "MinimalTask()"


def test_interaction_base_repr_defaults_to_class_name() -> None:
    """Verify simple interactions have the shared activity fallback representation."""
    assert repr(MinimalInteraction()) == "MinimalInteraction()"


def test_consequence_base_repr_defaults_to_class_name() -> None:
    """Verify simple consequences have the shared activity fallback representation."""
    assert repr(MinimalConsequence()) == "MinimalConsequence()"


def test_api_task_reprs_are_concise_and_safe() -> None:
    """Verify API task reprs avoid noisy payload dumps and secret leakage."""
    assert repr(LoginToWorkItemsApi.with_credentials("stan", "super-secret")) == (
        "LoginToWorkItemsApi(username='stan')"
    )
    assert repr(CreateWorkItemViaApi.with_payload({"title": "Bug", "priority": "LOW"})) == (
        "CreateWorkItemViaApi(title='Bug', priority='LOW')"
    )
    assert repr(UpdateWorkItemViaApi.for_work_item(7, {"status": "COMPLETED"})) == (
        "UpdateWorkItemViaApi(work_item_id=7, status='COMPLETED')"
    )
    assert repr(DeleteWorkItemViaApi.for_work_item(9)) == "DeleteWorkItemViaApi(work_item_id=9)"


def test_api_question_reprs_are_concise_and_readable() -> None:
    """Verify API questions expose the small identifiers humans need in logs."""
    assert repr(FetchWorkItemsViaApi.all()) == "FetchWorkItemsViaApi(filter_name='all')"
    assert repr(FetchWorkItemViaApi.by_id(3)) == "FetchWorkItemViaApi(work_item_id=3)"
    assert repr(WorkItemExistsViaApi(4)) == "WorkItemExistsViaApi(work_item_id=4)"
    assert repr(WorkItemFieldEqualsViaApi(5, "status", "COMPLETED")) == (
        "WorkItemFieldEqualsViaApi(work_item_id=5, field_name='status', "
        "expected_value='COMPLETED')"
    )
    assert repr(WorkItemIdForTitleViaApi("Fix bug")) == (
        "WorkItemIdForTitleViaApi(title='Fix bug', filter_name='all')"
    )
