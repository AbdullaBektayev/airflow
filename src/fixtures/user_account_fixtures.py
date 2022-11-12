from typing import Tuple

import pytest

from model_bakery import baker


__all__: Tuple = (
    "user_account",
)

from django.contrib.auth.models import User
@pytest.fixture()
def user_account(db):  # pylint: disable=unused-argument
    def _user(**kwargs):
        return baker.make("auth.User", **kwargs)

    return _user

