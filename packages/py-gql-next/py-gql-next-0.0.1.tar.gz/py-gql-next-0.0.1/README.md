# python-graphql
Python client of GraphGL.This package mainly uses `requests` to build the http/https requests.

### Usage: 
(example of gitlab graphql api)
```python
from client import Client

headers = {"Private-Token": "gitlab token"}

# these params is send to requests, so you can pass kwargs to `Client`
client = Client(url="https://example.gitlab.com/api/graphql", headers=headers, verify=False)

query = {
    "query": """{
            currentUser {
                name
        }
    }"""
}

print(client.execute(query))
```
Result
```python
{'data': {'currentUser': {'name': 'Administrator'}}}
```
TODO:
- [ ] async support