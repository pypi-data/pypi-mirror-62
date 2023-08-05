# python-graphql
Python client of GraphGL.This package mainly uses `requests` to build the http/https requests.

### Install
```bash
pip install py-gql-next
```
### Usage: 
(example of gitlab graphql api)
```python
from pygql import Client

gitlab = Client(url="https://www.gitlab.com/api/graphql")

query = {
    "query": """
    {
        currentUser {
            name
        }
    }"""
}

print(gitlab.execute(query))
```
Result
```json
{
    "data": {
        "currentUser": None
    }
}
```
TODO:
- [ ] async support
- [x] add tests