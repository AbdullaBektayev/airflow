from rest_framework import status
from rest_framework.reverse import reverse


def test_provider_a_api_get_success(db, unauthorized_api_client, json_data_by_path, mocker):
    mocked_sleep = mocker.patch(
        "src.apps.flights.api.v1.views.provider_views.GenericProviderCreateAPIView._sleep_time", return_value="rqwerw"
    )

    response = unauthorized_api_client.post(reverse("api-v1-flights:provider-a-search"))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == json_data_by_path("./src/apps/flights/helper_data/response_a.json")
    mocked_sleep.assert_called_once()


def test_provider_b_api_get_success(db, unauthorized_api_client, json_data_by_path, mocker):
    mocked_sleep = mocker.patch(
        "src.apps.flights.api.v1.views.provider_views.GenericProviderCreateAPIView._sleep_time", return_value=None
    )

    response = unauthorized_api_client.post(reverse("api-v1-flights:provider-b-search"))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == json_data_by_path("./src/apps/flights/helper_data/response_b.json")
    mocked_sleep.assert_called_once()
