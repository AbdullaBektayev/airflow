from src.apps.flights.models import AirflowSearch


def test_core_queryset_activate(db, airflow_search):
    assert AirflowSearch.objects.count() == 0

    user = airflow_search(is_active=False)

    assert AirflowSearch.objects.count() == 1
    assert AirflowSearch.objects.active().count() == 0
    assert AirflowSearch.objects.inactive().count() == 1
    assert AirflowSearch.objects.inactive().first() == user

    user.activate()

    assert AirflowSearch.objects.count() == 1
    assert AirflowSearch.objects.active().count() == 1
    assert AirflowSearch.objects.inactive().count() == 0
    assert AirflowSearch.objects.active().first() == user


def test_core_queryset_deactivate(db, airflow_search):
    assert AirflowSearch.objects.count() == 0

    user = airflow_search(is_active=True)

    assert AirflowSearch.objects.count() == 1
    assert AirflowSearch.objects.active().count() == 1
    assert AirflowSearch.objects.inactive().count() == 0
    assert AirflowSearch.objects.active().first() == user

    user.deactivate()

    assert AirflowSearch.objects.count() == 1
    assert AirflowSearch.objects.active().count() == 0
    assert AirflowSearch.objects.inactive().count() == 1
    assert AirflowSearch.objects.inactive().first() == user
