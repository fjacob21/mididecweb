from bs4 import BeautifulSoup
from src.users import Users
from src.stores import MemoryStore
from src.email_generators import UserResetPasswordEmail


def test_user_validation_email():
    store = MemoryStore()
    users = Users(store)
    u = users.add("test@test.com", 'name', 'alias', 'psw', 8)
    email = UserResetPasswordEmail('', '', root='./src')
    html = email.generate(u)
    soup = BeautifulSoup(html, 'html.parser')
    assert html
    assert type(html) == str
    assert bool(soup.find())
