from typing import Optional, TypeVar, Callable, TypedDict, cast, Generic, Union
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
    
    def map_if(self, cn: Callable[[T], bool], tr: Union[Callable[[T], T],Callable[[T, Pipe[T]], T]]):
        for i in range(len(self.items)):
            if cn(self.items[i]):
                try:
                    self.items[i] = tr(self.items[i], self) # pyright: ignore[reportCallIssue]
                except TypeError:
                    self.items[i] = tr(self.items[i]) # pyright: ignore[reportCallIssue]
                
        return self
    
    def map(self, fn: Union[Callable[[T], T],Callable[[T, Pipe[T]], T]]):
        for i in range(len(self.items)):
            try:
                self.items[i] = fn(self.items[i], self) # pyright: ignore[reportCallIssue]
            except TypeError:
                self.items[i] = fn(self.items[i]) # pyright: ignore[reportCallIssue]
        return self
    
    def filter(self, fn: Union[Callable[[T], bool], Callable[[T, Pipe[T]], bool]]):
        nitems: list[T] = []
        
        for i in range(len(self.items)):
            try:
                if fn(self.items[i], self): # pyright: ignore[reportCallIssue]
                    nitems.append(self.items[i])
            except TypeError:
                if fn(self.items[i]): # pyright: ignore[reportCallIssue]
                    nitems.append(self.items[i])
                
        return Pipe(nitems)

    def to_list(self):
        return self.items
    
    def find(self, fn: Union[Callable[[T], bool], Callable[[T, Pipe[T]], bool]]) -> Optional[T]:
        for item in self.items:
            try:
                if fn(item, self): # pyright: ignore[reportCallIssue]
                    return item
            except TypeError:
                if fn(item): # pyright: ignore[reportCallIssue]
                    return item
        return None
    
