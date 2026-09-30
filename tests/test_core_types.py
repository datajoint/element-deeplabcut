"""Every column in every table definition must use a DataJoint 2.x core type or codec.

Parses the package source as text (no database needed) and classifies each attribute type with
DataJoint's own ``match_type``, so native MySQL types (``int``, ``float``, ``longblob``, ...) cannot
creep back in.
"""

import ast
import pathlib
import re

from datajoint.declare import CORE_TYPE_NAMES, match_type

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {"tests", "docs", "notebooks", ".git", ".venv"}


def _source_files():
    for path in REPO_ROOT.rglob("*.py"):
        if not SKIP_DIRS.intersection(path.relative_to(REPO_ROOT).parts):
            yield path


def _definition_strings(tree):
    """Yield (lineno, text) for every ``definition = ...`` string in the module."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "definition" for t in node.targets):
            continue
        value = node.value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            yield node.lineno, value.value
        elif isinstance(value, ast.JoinedStr):
            parts = [v.value if isinstance(v, ast.Constant) else "{}" for v in value.values]
            yield node.lineno, "".join(parts)


def _attribute_types(definition):
    """Yield the declared type of each attribute line in a definition."""
    for line in definition.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith(("---", "->", "-", "index", "unique")) or ":" not in line:
            continue
        # a default value may contain ':' only when quoted; strip quoted strings first
        unquoted = re.sub(r"(\"[^\"]*\"|'[^']*')", "''", line)
        yield unquoted.split(":", 1)[1].strip()


def _is_core_or_codec(attribute_type):
    if attribute_type == "{}":  # type supplied by an f-string placeholder
        return True
    try:
        category = match_type(attribute_type)
    except Exception:
        return False
    return category in CORE_TYPE_NAMES or category == "CODEC"


def find_non_core_types():
    found = []
    for path in _source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for lineno, definition in _definition_strings(tree):
            for attribute_type in _attribute_types(definition):
                if not _is_core_or_codec(attribute_type):
                    found.append(f"{path.relative_to(REPO_ROOT)}:{lineno}: {attribute_type}")
    return found


def test_all_columns_use_core_types():
    assert not find_non_core_types()


if __name__ == "__main__":
    print("\n".join(find_non_core_types()) or "all core types")
