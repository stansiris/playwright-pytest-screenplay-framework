from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.core.question import Question


class FocusIndicatorVisible(Question):
    """Question: whether the active element has a visible focus indicator."""

    def answered_by(self, actor) -> bool:
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
        return "FocusIndicatorVisible()"
