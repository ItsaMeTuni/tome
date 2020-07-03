def test_strength():
    # TODO(pxeger) better testing for password strength
    import tome.controllers.password

    assert tome.controllers.password.strength(
        "hunter2"
    ) < tome.controllers.password.strength("Sup3r5ECr€tt!")


def test_hash_verify():
    import tome.controllers.password

    hash_ = tome.controllers.password.hash_password("hunter2")
    assert hash_
    assert tome.controllers.password.verify_password(hash_, "hunter2")
    assert not tome.controllers.password.verify_password(hash_, "incorrect")


def test_rehash():
    import argon2
    import tome.controllers.password

    time_cost = tome.controllers.password._hasher.time_cost
    # definitely different parameters
    hasher = argon2.PasswordHasher(time_cost=time_cost + 1)
    hash_needs_rehash = hasher.hash("hunter2")
    assert tome.controllers.password.rehash("hunter2", hash_needs_rehash)
    hash_doesnt_need_rehash = tome.controllers.password.hash_password("hunter2")

    assert (
            tome.controllers.password.rehash("hunter2", hash_doesnt_need_rehash) is None
    )
