import json
import os
from typing import Optional, TypeVar, Iterable, Callable, TypedDict, cast

class User(TypedDict):
    firstname: str
    lastname: str
    username: str
    email: str
    age: int
    id: int

T = TypeVar("T")

def find(iter: Iterable[T], fn: Callable[[T], bool]) -> Optional[T]:
    for item in iter:
        if fn(item):
            return item
    return None
    

with open(os.path.join('db', 'users.json')) as f:
    data = cast(list[User], json.load(f))
    
print('Users:')


user20 = find(data, lambda x: x['id'] == 3)




print(user20)
