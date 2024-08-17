from model.user import User
from errors import Missing, Duplicate


_users = [
    User(name='resident_evil', hash='abc'),
    User(name='silent_hill', hash='xyz'),
]

def find(name: str) -> User | None:
    for _user in _users:
        if _user.name == name:
            return _user
    return None

def check_missing(name: str) -> None:
    if not find(name=name):
        raise Missing(msg=f'Missing user {name}')

def check_duplicate(name: str) -> None:
    if find(name=name):
        raise Duplicate(msg=f'Duplicate user {name}')
    
def get_all() -> list[User]:
    return _users

def get_one(name: str) -> User | None:
    check_missing(name=name)
    return find(name=name)

def create(user: User) -> User:
    check_duplicate(name=user.name)
    return user

def modify(name: str, user: User) -> User:
    check_missing(name=name)
    return user

def delete(name: str) -> bool:
    check_missing(name=name)
    return True