from copy import deepcopy
from typing import Any

def _traverse_for_set(data: dict, parts: list) -> Any:
    """
    Internal recursive helper for `set_`.
    Navigates or creates path segments.
    """
    head, *tail = parts

    # Handle list index creation/access
    if head.isdigit():
        head = int(head)
        # This part is complex. For simplicity, we assume lists are not created on the fly.
        # A full implementation would need to decide whether to create a list or dict.
        # We will focus on dict creation for this example.
        raise NotImplementedError("On-the-fly list creation is not supported in this simple version.")

    if not tail:
        return # Parent found, return to set the value.

    # Ensure the next level is a dictionary
    if head not in data or not isinstance(data[head], dict):
        data[head] = {}

    return _traverse_for_set(data[head], tail)


def set_(data: Any, path: str, value: Any) -> Any:
    new_data = deepcopy(data)
    parts = path.split('.')

    # Can't set a value on a non-dict root (unless replacing it, which is not set's job)
    if not isinstance(new_data, dict):
        raise TypeError("set_ can only operate on a dictionary-like root object.")

    current = new_data
    for part in parts[:-1]:
        if part.isdigit(): # List access
            idx = int(part)
            if isinstance(current, list) and 0 <= idx < len(current):
                current = current[idx]
            else: # Path does not exist
                raise IndexError(f"Path segment '{part}' is out of range or not a list.")
        else: # Dict access
            current = current.setdefault(part, {})

    last_part = parts[-1]
    if last_part.isdigit():
        idx = int(last_part)
        if isinstance(current, list):
            if idx >= len(current):
                current.extend([None] * (idx - len(current) + 1))
            current[idx] = value
        else: # Cannot use numeric index on a dict
            current[last_part] = value
    else:
        current[last_part] = value

    return new_data

def delete_(data: Any, path: str) -> Any:
    new_data = deepcopy(data)
    parts = path.split('.')
    current = new_data

    for part in parts[:-1]:
        try:
            current = current[int(part)] if part.isdigit() else current[part]
        except (KeyError, IndexError, TypeError):
            return new_data # Path doesn't exist, nothing to delete

    last_part = parts[-1]
    try:
        if isinstance(current, list) and last_part.isdigit():
            del current[int(last_part)]
        elif isinstance(current, dict):
            del current[last_part]
    except (KeyError, IndexError):
        pass # Target doesn't exist, do nothing

    return new_data

def _find_target_for_update(data: Any, path: str) -> Any:
    """Helper to navigate to a target for update/append."""
    parts = path.split('.')
    current = data
    for part in parts:
        try:
            current = current[int(part)] if part.isdigit() else current[part]
        except (KeyError, IndexError, TypeError):
            return None # Path not found
    return current

def update_(data: Any, path: str, value: dict) -> Any:
    new_data = deepcopy(data)
    target = _find_target_for_update(new_data, path)
    if isinstance(target, dict) and isinstance(value, dict):
        target.update(value)
    return new_data

def append_(data: Any, path: str, value: Any) -> Any:
    new_data = deepcopy(data)
    target = _find_target_for_update(new_data, path)
    if isinstance(target, list):
        target.append(value)
    return new_data