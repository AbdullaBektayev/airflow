from typing import Tuple

import pytest

from model_bakery import baker


__all__: Tuple = ("airflow_search", "airflow_search_kc")

from src.apps.flights.models import AirflowSearch


@pytest.fixture()
def airflow_search(db):  # pylint: disable=unused-argument
    def _airflow_search(**kwargs):
        return baker.make("flights.AirflowSearch", **kwargs)

    return _airflow_search


@pytest.fixture()
def airflow_search_kc(db):  # pylint: disable=unused-argument
    return baker.make("flights.AirflowSearch", state=AirflowSearch.COMPLETED)
