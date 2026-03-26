from typing import Optional, TypeVar, Callable, Generic, Union

T = TypeVar("T")

U = TypeVar('U')

class pipe(Generic[T]):
    def __init__(self, items: list[T]):
        self.items = items.copy()
    
    def map_if(self, cn: Callable[[T], bool], tr: Union[Callable[[T], T], Callable[[T, "pipe[T]"], T]]):
        for i in range(len(self.items)):
            if cn(self.items[i]):
                try:
                    self.items[i] = tr(self.items[i], self) # pyright: ignore[reportCallIssue]
                except TypeError:
                    self.items[i] = tr(self.items[i]) # pyright: ignore[reportCallIssue]
                
        return self
    
    def map(self, fn: Union[Callable[[T], U], Callable[[T, "pipe[T]"], U]]) -> "pipe[U]":
        new_items: list[U] = []
        for item in self.items:
            try:
                new_items.append(fn(item, self)) # type: ignore
            except TypeError:
                new_items.append(fn(item)) # type: ignore
                
        return pipe(new_items)
    
    def filter(self, fn: Union[Callable[[T], bool], Callable[[T, "pipe[T]"], bool]]):
        nitems: list[T] = []
        
        for i in range(len(self.items)):
            try:
                if fn(self.items[i], self): # pyright: ignore[reportCallIssue]
                    nitems.append(self.items[i])
            except TypeError:
                if fn(self.items[i]): # pyright: ignore[reportCallIssue]
                    nitems.append(self.items[i])
                
        return pipe(nitems)

    def to_list(self):
        return self.items
    
    def find(self, fn: Union[Callable[[T], bool], Callable[[T, "pipe[T]"], bool]]) -> Optional[T]:
        for item in self.items:
            try:
                if fn(item, self): # pyright: ignore[reportCallIssue]
                    return item
            except TypeError:
                if fn(item): # pyright: ignore[reportCallIssue]
                    return item
        return None
