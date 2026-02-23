# Design Decisions

## Why Step One Has No Page-Specific Questions

Step One only performs validation. Generic Questions
(ValueOf, TextOf, IsVisible) are sufficient.

## Why TotalsMatchComputedSum Exists

Overview page contains business logic (math).
Encapsulating total validation prevents duplication.

## Why AddItem Is Context-Aware

Tests should not expose page location.
Task resolves locator internally.