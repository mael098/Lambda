from typing import Optional, TypeVar, Callable, TypedDict, cast, Generic
import json
import os

class User(TypedDict):
    firstname: str
    lastname: str
    username: Optional[str]
    email: str
    age: int
    id: int

T = TypeVar("T")

with open(os.path.join('db', 'users.json')) as f:
    data = cast(list[User], json.load(f))
    
class Pipe(Generic[T]):
    def __init__(self, items: list[T]):
        self.process = []
        self.items = items
    
    def map_if(self, cn: Callable[[T], bool], tr: Callable[[T], T]):
        for i in range(len(self.items)):
            if cn(self.items[i]):
                self.items[i] = tr(self.items[i])
        return self
    
    def map(self, fn: Callable[[T], T]):
        self.items = list(map(fn, self.items))
        return self
    
    def filter(self, fn: Callable[[T], bool]):
        self.items = list(filter(fn, self.items))
        return self

    def to_list(self):
        return list(self.items)
    
    def find(self, fn: Callable[[T], bool]) -> Optional[T]:
        for item in self.items:
            if fn(item):
                return item
        return None