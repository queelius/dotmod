# `dotmod` - Immutable Modifications for Nested Data Structures

> "To improve is to change; to be perfect is to change often."  
>
> — Winston Churchill

**Immutable modifications for nested data structures.**

```python
>>> from dotmod import set_
>>> data = {"user": {"name": "Alice", "status": "active"}}
>>> new_data = set_(data, "user.status", "inactive")
>>>
>>> new_data['user']['status']
'inactive'
>>> data['user']['status'] # Original data is unchanged
'active'
```

## Why?

The `dot` ecosystem provides powerful tools for reading and transforming data. `dotmod` provides the essential counterpart: **writing data**.

It does so with two core principles:

1. **Immutability:** It never changes your original data. Every function returns a modified deep copy, eliminating side effects and making state changes predictable and safe.
2. **Clarity:** It provides simple, explicit verbs for modification. When you read `set_` or `delete_`, the intent is unmistakable.

## The Four Verbs of Change

`dotmod` provides four functions, covering the fundamental ways to alter a data structure.

```python
from dotmod import set_, delete_, update_, append_

data = {"users": [{"name": "Alice", "roles": ["guest"]}]}

# set_: Changes an existing value or creates a new path/value.
data_v2 = set_(data, "users.0.name", "Alice Liddell")

# delete_: Removes a key from an object or an item from a list.
data_v3 = delete_(data_v2, "users.0.roles")

# update_: Merges a dictionary into an existing one.
# Here we add the roles back, plus a new status field.
data_v4 = update_(data, "users.0", {"roles": ["admin"], "status": "active"})

# append_: Adds an item to a list.
data_v5 = append_(data_v4, "users.0.roles", "auditor")
# data_v5 -> {'users': [{'name': 'Alice', 'roles': ['admin', 'auditor'], 'status': 'active'}]}
```

While this simple implementation uses basic dot paths, the *spirit* of the library is to work with any addressing tool. A full implementation would use `dotquery` to perform targeted modifications:

```python
# CONCEPTUAL: Set status for a user without knowing their index
# new_data = set_(data, "users[name=Alice Liddell].status", "archived")
```

## Command-Line Usage

`dotmod` can also be used as a command-line tool to modify JSON or YAML files.

The output format will match the input format.

### `set`

Set a value at a specific path.

```bash
# Set a user's status to "inactive" in a JSON file
cat data.json | dotmod set user.status '"inactive"' > new_data.json

# Set a value in a YAML file
dotmod set user.name '"Bob"' data.yml > new_data.yml
```

### `delete`

Delete a value at a specific path.

```bash
# Delete the user's status from a JSON file
cat data.json | dotmod delete user.status > new_data.json
```

### `update`

Merge an object at a specific path.

```bash
# Update a user's profile in a JSON file
cat data.json | dotmod update user '{"status": "inactive", "theme": "dark"}' > new_data.json
```

### `append`

Append a value to a list at a specific path.

```bash
# Append a role to a user in a JSON file
cat data.json | dotmod append user.roles '"auditor"' > new_data.json
```

## When to use `dotmod`

✅ You need to update a configuration object and save a new version.
✅ You want to change state in a predictable, immutable way for an application.
✅ You are building a component that needs to propose a change without causing side effects.

## When NOT to use `dotmod`

❌ You need to modify data in-place for performance reasons. Just use standard Python mutation.
❌ You have to perform a long sequence of changes that must be atomic. Use `dotbatch`.
❌ You are transforming data into a new shape. Use `dotpipe`.

## Philosophy

`dotmod` is the `sed` (stream editor) for your data. It provides the core, immutable editing verbs for the ecosystem. It's built on the idea that change should be explicit, safe, and easy to reason about.

## Install

```bash
pip install dotmod
```

## License

MIT. Use it freely.

