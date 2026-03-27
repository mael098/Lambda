from typing import Optional, TypedDict, cast
# from rich import print
import json
import os
from classes.pipe import pipe
import numpy as np
import matplotlib.pyplot as plt

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
"""
Se busca un usuario especifico por su id
"""
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
"""
Se filtran todos los usuarios mayores de 18 años
se le agrega un email a los que no tienen
y se normaliza el username colocandolo en minusculas
con el fin de simular un pipeline en un servidor
"""
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


print("-------------------------------------------------------------------------------------------------------")




matrix = np.array([
    [u['age'], 1 if u['email'] else 0]
    for u in normalized
], dtype=float)

print("\nMatriz de usuarios [edad, tiene_email]:")
print(matrix.tolist())


weights = np.array([1, 1]) # importancia de edad y email

scores = matrix @ weights

print("\nScore de usuarios:")
print(scores)
top_users = sorted(
    zip(normalized, scores),
    key=lambda x: x[1],
    reverse=True
)

print("\nTop usuarios:")
for user, score in top_users[:5]:
    print(user['username'], score)

plt.bar(range(len(scores)), scores) # type: ignore
plt.title("Score de usuarios")# type: ignore
plt.xlabel("Usuario")# type: ignore
plt.ylabel("Score")# type: ignore
plt.show()# type: ignore