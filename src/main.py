from typing import Optional, TypedDict, cast
from rich import print
import json
import os
from classes.pipe import pipe

class User(TypedDict):
    firstname: str
    lastname: str
    username: str
    email: Optional[str]
    age: int
    id: int

with open(os.path.join('db', 'users.json')) as f:
    data = cast(list[User], json.load(f))

# ----------------------------
# ----------- FIND -----------
# ----------------------------
user30 = pipe(data).find(lambda u: u['id'] == 30)

print('User 30')
print(json.dumps(user30, indent=4))

# ----------------------------
# ------- FILTER y MAP -------
# ----------------------------
"""
Se toman los usuarios sin correo como anonimos asi que se filtran
y por ultimo se mapean para mostrar unicamente su nombre de usuario
"""
anonimous = pipe(data)\
    .filter(lambda u: not u['email'])\
    .map(lambda u: u['username'])\
    .to_list()

print()
print('Usuarios anonimos:')
print(anonimous)

# ----------------------------
# --- FILTER, MAP Y MAP_IF ---
# ----------------------------
normalized = pipe(data)\
    .filter(lambda u: u['age'] >= 18)\
    .map_if(
        lambda u: not u['email'], 
        lambda u: { 
            **u, 
            'email': f'{u['firstname'].lower()}_{u['lastname'].lower()}@enterprice.com' 
        }
    )\
    .map(lambda u: { 
        **u, 
        'username': u['username'].lower()
    })\
    .to_list()
    
print()
print('Normalizados')
print(normalized)