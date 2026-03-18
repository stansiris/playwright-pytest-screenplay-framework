from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.playwright.browse_the_web import BrowseTheWeb


class FocusIndicatorVisible(Question):
    """Question: whether the active element has a visible focus indicator."""

    def answered_by(self, actor: Actor) -> bool:
        """Evaluate focus-ring visibility heuristics for the active element."""
        page = actor.ability_to(BrowseTheWeb).page
        return bool(
            page.evaluate(
                """
                () => {
                  const active = document.activeElement;
                  if (!active || active === document.body) {
                    return false;
                  }

                  if (active.matches(':focus-visible')) {
                    return true;
                  }

                  const style = window.getComputedStyle(active);
                  const hasOutline =
                    style.outlineStyle !== 'none' &&
                    style.outlineWidth !== '0px' &&
                    style.outlineColor !== 'rgba(0, 0, 0, 0)';
                  const hasShadow = style.boxShadow && style.boxShadow !== 'none';

                  return Boolean(hasOutline || hasShadow);
                }
                """
            )
        )

    def __repr__(self) -> str:
        """Return a compact representation for logs."""
        return "FocusIndicatorVisible()"
