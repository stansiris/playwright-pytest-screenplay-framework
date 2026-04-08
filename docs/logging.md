# Logging Conventions

This project keeps Screenplay logging intentionally simple.

The logging layer should answer only a few questions:

- Who is acting?
- What are they doing?
- Did it start, finish, or fail?
- If it failed, what was the error?

Everything else should stay secondary.

## Current Log Style

`Actor` logging is driven by `log_screenplay_step` in `screenplay_core/lifecycle/decorators.py`.

Questions log in this style:

```text
Customer asks CurrentUrl()
Customer got CurrentUrl() -> "https://www.saucedemo.com/inventory.html" (12 ms)
Customer failed CurrentUrl() after 5000 ms: Customer does not have ability BrowseTheWeb.
```

Activities log in this style:

```text
Customer starts Click(target='Login button')
Customer ends Click(target='Login button') (18 ms)
Customer failed Click(target='Login button') after 5000 ms: Customer does not have ability BrowseTheWeb.
```

## Core Idea

The decorator handles lifecycle:

- `asks` / `got` / `failed` for `Question`
- `starts` / `ends` / `failed` for `Activity`

The Screenplay object itself provides meaning through `__repr__`.

That means:

- decorator = lifecycle
- `__repr__` = human-readable step label

## Why `__repr__` Matters

The decorator does not know the business meaning of a `Task`, `Interaction`, or `Question`.
It only knows that an object is being executed.

The object's `__repr__` tells the human reader what that object represents.

Examples:

- `CurrentUrl()`
- `Click(target='Login button')`
- `Fill(target='Password', text='********')`
- `Ensure(target='Error message', assertion='to_have_text', args=('Epic sadface',))`

If `__repr__` is weak, the logs are weak.
If `__repr__` is clear, the logs are clear.

## `__repr__` Guidelines

Use `ClassName(...)` format for concrete `Task`, `Interaction`, and `Question` classes.

Prefer:

- target descriptions
- usernames
- short titles
- IDs
- short URLs
- other business-facing values

Avoid:

- passwords
- tokens
- cookies
- raw secrets
- full request payloads
- large blobs of text
- low-level locator internals
- unstable memory-address style output

Keep `__repr__`:

- single-line
- short
- stable
- readable by a human scanning test logs

## Good Examples

```python
def __repr__(self) -> str:
    return "CurrentUrl()"
```

```python
def __repr__(self) -> str:
    return f"Click(target={self.target.description!r})"
```

```python
def __repr__(self) -> str:
    return f"Login(username={self.username!r})"
```

```python
def __repr__(self) -> str:
    return f"WorkItemIdForTitle(title={self.title!r})"
```

## Bad Examples

Too noisy:

```python
def __repr__(self) -> str:
    return f"{self.__dict__}"
```

Leaks secrets:

```python
def __repr__(self) -> str:
    return f"Login(username={self.username!r}, password={self.password!r})"
```

Unhelpful:

```python
def __repr__(self) -> str:
    return self.__class__.__name__
```

## Fallback Behavior

If a class does not define a useful `__repr__`, the logging helper falls back to the class name.

That is acceptable for small or temporary classes, but production-quality Screenplay objects should
usually provide a meaningful `__repr__`.

## Rule Of Thumb

When writing `__repr__`, ask:

> If this line appears in a failing test log, will a human understand what step was being executed?

If the answer is no, improve the representation.
