"""Tests for hello function."""
# import pytest

from svaeva_redux.schemas.redis import UserModel
from svaeva_redux.schemas.utils import update_user_avatar, update_user_conversation_embedding


# @pytest.mark.parametrize(
#     ("name", "expected"),
#     [
#         ("Jeanette", "Hello Jeanette!"),
#         ("Raven", "Hello Raven!"),
#         ("Maxine", "Hello Maxine!"),
#         ("Matteo", "Hello Matteo!"),
#         ("Destinee", "Hello Destinee!"),
#         ("Alden", "Hello Alden!"),
#         ("Mariah", "Hello Mariah!"),
#         ("Anika", "Hello Anika!"),
#         ("Isabella", "Hello Isabella!"),
#     ],
# )
def test_user():
    """Example test with parametrization."""
    pk = "123456"
    user = UserModel(
        id=pk,
        group_id="group_id",
        platform_id="platform_id",
        interaction_count=1,
        first_name="first_name",
        last_name="last_name",
        username="username",
        description="description",
        phone_number="+1234567890",
        email="email",
        register_method="register_method",
        country="US",
        avatar_image_bytes=bytes("avatar_image_bytes", "utf-8"),
    )
    user.save()
    user = UserModel.get(pk)
    assert user.id == pk
    assert user.group_id == "group_id"
    assert user.platform_id == "platform_id"
    assert user.interaction_count == 1
    assert user.first_name == "first_name"
    assert user.last_name == "last_name"
    assert user.username == "username"
    assert user.description == "description"
    assert user.phone_number == "+1234567890"
    assert user.email == "email"
    assert user.register_method == "register_method"
    assert user.country == "US"


def test_user_update():
    pk = "123456"
    update_user_avatar(pk, bytes("avatar_image_bytes", "utf-8"))


def test_user_update_embedding():
    pk = "123456"
    update_user_conversation_embedding(pk, [1, 2, 3])

    # user.delete(pk)

    # from redis_om.model.model import NotFoundError

    # try:
    #     user = UserModel.get(pk)
    # except NotFoundError:
    #     user = None
    # assert user is None
