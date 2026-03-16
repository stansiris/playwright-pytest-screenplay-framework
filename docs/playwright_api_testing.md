# Playwright API Testing — Concepts & Mental Models

## The Two Worlds in Playwright

Playwright has two distinct ways to make HTTP calls. Understanding which world you are in determines what features are available to you.

---

## World 1: The Browser World (`BrowserContext` + `page`)

This is the full browser stack. Playwright launches a real browser (Chromium, Firefox, WebKit), which manages:

- A **`BrowserContext`** — an isolated browser session (cookies, storage, network)
- One or more **`Page`** objects — individual tabs inside that context

```
Browser
  └── BrowserContext  (cookie jar, base_url, network interception)
        └── Page      (tab — renders HTML, runs JS, fires requests)
              └── page.request  (APIRequestContext backed by BrowserContext)
```

### Key points

- All pages inside the same `BrowserContext` **share the same cookie jar**
- `page.request` is an `APIRequestContext` that is **backed by the BrowserContext** — it inherits `base_url`, cookies, and headers from it
- Because it lives inside the browser network stack, it supports **request interception via `route()`**

---

## World 2: The Standalone HTTP World (`playwright.request`)

This is a pure HTTP client — no browser, no DOM, no rendering. Think of it as `requests.Session` but Playwright-flavoured.

```
playwright.request.new_context()
  └── APIRequestContext  (plain HTTP client — no browser behind it)
```

### Key points

- Lightweight — no browser process launched
- Has its own cookie jar, but it is **not shared** with any browser context
- Does **not** support `route()` — there is no browser network stack to intercept
- Best for pure API tests that do not need a UI

---

## The Two APIRequestContext Flavours

`APIRequestContext` is the same class in both worlds, but **where it comes from** determines its capabilities:

| Source | How created | Shares browser cookies | Supports `route()` |
|--------|-------------|----------------------|-------------------|
| `page.request` | automatically, from `Page` | ✓ yes — same `BrowserContext` | ✓ yes |
| `context.request` | automatically, from `BrowserContext` | ✓ yes — same `BrowserContext` | ✓ yes |
| `playwright.request.new_context()` | manually, standalone | ✗ no — isolated | ✗ no |

In this project:

- `api` fixture → `playwright.request.new_context()` → standalone, no cookie sharing, no routing
- `logged_in_taskhub_customer` fixture → `page.request` → shares cookies with the browser session

---

## APIResponse

`APIResponse` is the object returned by any HTTP call (`.get()`, `.post()`, etc.) regardless of which world you are in.

| Property / Method | What it gives you |
|-------------------|-------------------|
| `response.ok` | `True` if status is 2xx |
| `response.status` | Raw HTTP status code (200, 401, 404…) |
| `response.json()` | Parsed JSON body |
| `response.text()` | Raw text body |
| `response.headers` | Response headers dict |

---

## Request Interception: `route()`

`route()` registers a handler that fires **before** a matching request reaches the server. It is only available in the browser world.

```
Test                 Playwright (browser network stack)        Server
 |                              |                                 |
 | page.route("**/api/tasks")   |                                 |
 |----------------------------->| registered                      |
 |                              |                                 |
 | (request fires)              |                                 |
 |                              | handler called with Route obj   |
 |                              |                                 |
 |                              |-- route.fulfill() ------------->| (server never called)
 |                              |-- route.continue_() ----------->| (server called normally)
 |                              |-- route.abort() --------------->| (network error simulated)
```

### The `Route` object

The handler receives a `Route` object — it represents the **intercepted outgoing request**.

```python
def handle(route: Route) -> None:
    print(route.request.url)      # URL being requested
    print(route.request.method)   # GET, POST, etc.
    print(route.request.headers)  # request headers
    print(route.request.post_data) # request body

    route.fulfill(status=404, json={"error": "Not found."})
```

### `route()` scope

| Where registered | Intercepts |
|-----------------|------------|
| `page.route()` | requests from that specific page only |
| `context.route()` | requests from all pages in the `BrowserContext` |

### When to use `route()`

- Simulating error states (404, 401, 500) without engineering the server into that state
- Testing UI behaviour under slow or failed network conditions (`route.abort()`)
- Avoiding test data setup for edge cases

---

## Cookie Sharing — The Key to Hybrid Tests

Because `page.request` shares the `BrowserContext` cookie jar, logging in via the UI automatically authenticates subsequent API calls — and vice versa.

### UI login → API call

```python
# 1. Actor logs in via the UI form — Flask sets Set-Cookie: session=...
customer.attempts_to(LoginToTaskHub.with_credentials("admin", "admin123"))

# 2. page.request carries the session cookie automatically
response = actor.ability_to(BrowseTheWeb).page.request.get("/api/me")
# → {"username": "admin"}  ✓
```

### API login → UI navigation

```python
# 1. POST to login API — cookie stored in BrowserContext
page.request.post("/api/login", data={"username": "admin", "password": "admin123"})

# 2. Navigate via browser — cookie sent automatically
page.goto("/tasks")  # already authenticated ✓
```

This is the foundation of **hybrid tests** — fast API setup, rich UI assertions — all within the same `BrowserContext` session.

---

## Summary Cheatsheet

```
                    ┌─────────────────────────────────────────────┐
                    │              Browser World                   │
                    │                                              │
                    │  BrowserContext                              │
                    │    ├── cookie jar  ◄──── shared by all      │
                    │    ├── base_url                              │
                    │    ├── route()  ◄────── interception        │
                    │    └── Page                                  │
                    │          └── page.request                    │
                    │               (APIRequestContext)            │
                    └─────────────────────────────────────────────┘

                    ┌─────────────────────────────────────────────┐
                    │           Standalone HTTP World              │
                    │                                              │
                    │  playwright.request.new_context()            │
                    │    └── APIRequestContext                     │
                    │         ✗ no route()                        │
                    │         ✗ no shared cookies                 │
                    │         ✓ lightweight, no browser           │
                    └─────────────────────────────────────────────┘

                    Both return APIResponse from HTTP calls.
```
