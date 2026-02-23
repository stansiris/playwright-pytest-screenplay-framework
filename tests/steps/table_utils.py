from collections.abc import Sequence


def as_row_dicts(datatable: Sequence[Sequence[object]]) -> list[dict[str, str]]:
    """Convert a pytest-bdd `datatable` raw matrix into row dictionaries."""
    if not datatable:
        return []

    headers = [str(cell).strip() for cell in datatable[0]]
    row_dicts: list[dict[str, str]] = []

    for row in datatable[1:]:
        values = [str(cell).strip() for cell in row]
        row_dicts.append(dict(zip(headers, values)))

    return row_dicts
