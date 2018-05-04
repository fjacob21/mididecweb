from src.bcrypt_hash import BcryptHash


def test_bcrypt_encrypt():
    password = BcryptHash('password').encrypt()
    assert password
    assert type(password) == str
    password2 = BcryptHash('password', password.encode()).encrypt()
    assert password2
    assert password2 == password
    password3 = BcryptHash('badpassword', password.encode()).encrypt()
    assert password3
    assert password3 != password
