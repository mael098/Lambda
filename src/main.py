from typing import Optional, TypedDict, cast
import json
import os
from classes.pipe import Pipe

class User(TypedDict):
    firstname: str
    lastname: str
    username: Optional[str]
    email: str
    age: int
    id: int

with open(os.path.join('db', 'users.json')) as f:
    data = cast(list[User], json.load(f))

Pipe([])
    