dotmodImmutable modifications for dot paths.>>> from dotmod import set_
>>> data = {"user": {"name": "Alice", "status": "active"}}
>>> new_data = set_(data, "user.status", "inactive")
>>> new_data['user']['status']
'inactive'
Why?The dot ecosystem provides powerful tools for reading data. dotmod provides the missing piece: writing data.It does so safely and predictably by providing simple verbs for immutable modifications. It never changes your original data; it always returns a modified copy.Installpip install dotmod
The Four Verbs of Changedotmod provides four functions. Think of them as the core verbs for Create, Update, and Delete.from dotmod import set_, delete_, update_, append_

data = {"users": [{"name": "Alice", "roles": ["guest"]}]}

# set_: Change an existing value or create a new one
data_v2 = set_(data, "users.0.name", "Alice L.")

# delete_: Remove a key or an item from a list
data_v3 = delete_(data_v2, "users.0.roles")

# update_: Merge a dictionary into an existing one
# Let's add the roles back, plus more info
data_v4 = update_(data, "users.0", {"roles": ["admin"], "status": "active"})

# append_: Add an item to a list
data_v5 = append_(data_v4, "users.0.roles", "auditor")
# data_v5 -> {'users': [{'name': 'Alice', 'roles': ['admin', 'auditor'], 'status': 'active'}]}
```dotmod` understands `dotquery` paths, so you can perform targeted modifications:
```python
# Set the status for a specific user without knowing their index
data = set_(data, "users[name=Alice].status", "archived")
When to use dotmod✅ You need to update a configuration file and save a new version.✅ You want to change state in a predictable, immutable way.✅ You're creating a modified copy of a data structure.When NOT to use dotmod❌ You need to modify data in-place (mutably). Just use standard Python.❌ You have to perform a long sequence of changes. Use dotbatch.❌ You are transforming data into a new shape. Use dotpipe.Philosophydotmod is the sed (stream editor) for your data. It provides the core editing verbs for the ecosystem. It's built on the idea that change should be explicit and safe. By always returning a copy, it avoids side effects and makes your code easier to reason about.LicenseMIT. Use it freely."To improve is to change; to be perfect is to change often." - Winston Churchill
