from typing import Literal, Optional, cast

from argon2 import PasswordHasher  # type: ignore
from argon2.exceptions import VerifyMismatchError  # type: ignore

from tome.exceptions import HTTPException

_hasher = PasswordHasher()

hash_password = _hasher.hash


def verify_password(hash_: str, password: str) -> bool:
    try:
        _hasher.verify(hash_, password)
    except VerifyMismatchError:
        return False
    else:
        return True


def rehash(password: str, hash_: str) -> Optional[str]:
    if _hasher.check_needs_rehash(hash_):
        return cast(str, _hasher.hash(password))
    return None


def strength(password: str) -> int:
    return len(set(password))


def check_password_strength(password: str) -> Literal[True]:
    if password == "beef stew":
        # easter egg
        raise HTTPException("Password not stroganoff", 418)
    elif strength(password) < 8:
        raise HTTPException("Password not strong enough", 422)
    elif any(map(" ".__gt__, password)):
        # control character
        raise HTTPException("Invalid character in password", 422)
    return True
