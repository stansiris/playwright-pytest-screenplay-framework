# API Testing Notes

This document records API-testing-specific design decisions, tradeoffs, and
open questions for the Screenplay framework.

It exists because API testing introduces a few tensions that are worth
documenting explicitly:

- Screenplay tests should stay behavior-oriented
- API tests still need real HTTP assertions
- the generic `Actor` should remain a generic orchestrator
- API-specific design choices will likely keep evolving

Use this document as the long-term home for API-testing-related architecture
notes and ADR-style decisions.

## Contents

- [Architecture Note: Raw API response ownership](#architecture-note-raw-api-response-ownership)
- [Architecture Note: Current transport choice](#architecture-note-current-transport-choice)
- [ADR-001: Store the latest raw API response on `CallTheApi`](#adr-001-store-the-latest-raw-api-response-on-calltheapi)
- [Open Topics](#open-topics)

---

## Architecture Note: Raw API response ownership

### Problem

API tests in this project still use the Screenplay pattern:

- Tasks perform API actions
- Questions read API state
- `Actor.attempts_to(...)` returns `None`

That creates a practical problem: a test may still need the raw HTTP
`requests.Response` for assertions such as:

- status code
- error payload
- raw JSON body
- transport-level behavior at the API boundary

### Current design

The latest raw HTTP `Response` is stored on the generic HTTP ability,
`CallTheApi`, as `last_response`.

Example:

```python
work_items_api_actor.attempts_to(
    LoginToWorkItemsApi.with_credentials("admin", "admin123"),
    CreateWorkItemViaApi.with_payload({"title": "Example"}),
)

response = work_items_api_actor.ability_to(CallTheApi).last_response
assert response is not None
assert response.status_code == 201
```

### Why this is the current compromise

This keeps response ownership at the layer that actually performs the HTTP
request.

We intentionally did not store response state on:

- the `Actor`, because `Actor` should remain a generic orchestrator
- API task objects, because Tasks should model actions rather than become
  mutable result containers
- a Work Items-specific memory helper, because that adds another layer and
  makes the runtime flow harder to follow

`CallTheApi` is the narrowest reasonable place to keep the latest raw HTTP
response while preserving the Screenplay structure.

### Recommended usage

- Use API Tasks for API actions
- Use API Questions for API reads and state checks
- Use `actor.ability_to(CallTheApi).last_response` only when the test needs a
  raw HTTP-level assertion

This keeps API tests in the Screenplay style while still allowing true API
testing.

### Important subtlety

API Questions also make HTTP calls through `CallTheApi`, so they overwrite
`CallTheApi.last_response` too.

That means:

- if multiple API Tasks run in a single `attempts_to(...)`, only the final raw
  response is preserved
- if an API Question runs after an API Task, the Question becomes the new
  `last_response`

Tests that need to assert on the raw response from a specific API Task should
do so immediately after that Task runs, before asking an API Question.

### Tradeoff

`last_response` is intentionally a latest-wins value.

This is acceptable for the current test style, but it is an explicit tradeoff
and may need to be revisited if future tests need richer response history.

---

## Architecture Note: Current transport choice

For now, API testing in this framework means plain HTTP through
`requests.Session`, not Playwright's `APIRequestContext`.

That is an intentional design choice.

Today the separation is:

- UI testing uses Playwright through `BrowseTheWeb`
- API testing uses HTTP through `CallTheApi`

Why this is the current direction:

- it keeps browser automation concerns separate from API transport concerns
- it keeps `CallTheApi` as a generic HTTP ability instead of tying it to
  Playwright
- it allows API tests to stand on their own as HTTP tests, rather than as
  browser-tooling-adjacent tests

This may be revisited in the future, but for now API testing here should be
understood as HTTP testing, not `APIRequestContext` testing.

---

## ADR-001: Store the latest raw API response on `CallTheApi`

### Status

Accepted

### Context

API tests in the Screenplay pattern need to assert on raw HTTP behavior such
as:

- status codes
- error payloads
- auth failures
- CRUD response bodies

However, `Actor.attempts_to(...)` returns `None`, so the raw `Response` from an
API Task is not directly returned to the test.

### Decision

Store the latest raw `requests.Response` on the `CallTheApi` ability as
`last_response`.

### Rationale

This decision preserves the intended responsibilities of the main Screenplay
components:

- `Actor` remains a generic orchestrator
- Tasks remain action-oriented
- Questions remain read-oriented
- `CallTheApi` owns HTTP transport concerns, so it is the best place to retain
  HTTP transport results

### Consequences

Benefits:

- API tests remain true Screenplay tests
- raw HTTP assertions remain possible
- response ownership stays close to the HTTP layer
- the design avoids task-result bags and actor-specific state

Tradeoffs:

- `last_response` is mutable shared state on the HTTP ability
- only the most recent API call is preserved
- later Tasks or Questions can overwrite it

### Alternatives considered

#### Store the response on the task

Rejected because Tasks become both actions and result containers, which makes
the execution flow harder to read.

#### Store the response on the actor

Rejected because `Actor` should stay generic and should not accumulate
API-specific state.

#### Store the response in a separate memory/helper object

Rejected because it adds another indirection and makes the API flow harder to
follow.

#### Avoid raw response access entirely

Rejected because API tests still need HTTP-level assertions to remain strong
API tests rather than only state-based integration checks.

---

## Open Topics

The current approach is intentionally small and practical, but this is not the
last API-testing design discussion we expect to have.

Potential future topics to record here:

- whether latest-wins `last_response` remains sufficient long-term
- whether some API assertions should move from raw responses into reusable
  Questions
