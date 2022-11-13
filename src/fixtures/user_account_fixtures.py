from typing import Tuple

import pytest

from model_bakery import baker
from django.contrib.auth.models import User


__all__: Tuple = (
    "user_account",
)


@pytest.fixture()
def user_account(db):  # pylint: disable=unused-argument
    def _user(**kwargs):
        return baker.make("auth.User", **kwargs)

    return _user

