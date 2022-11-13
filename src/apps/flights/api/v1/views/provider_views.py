import json

from time import sleep

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema

from src.apps.flights.api.v1.serializers.provider_serializer import ProviderSerializer


class GenericProviderCreateAPIView(CreateAPIView):
    json_file_path = None
    sleep_time = 30
    serializer_class = ProviderSerializer

    @staticmethod
    def _get_json_response(json_file_path):
        with open(json_file_path, mode="r") as file:
            json_data = json.load(file)
        return json_data

    def _get_json_file(self):
        if self.json_file_path is None:  # pragma: no cover
            raise ValueError("Doesn't have json file path")
        return self.json_file_path

    def _sleep_time(self):  # pragma: no cover
        return sleep(self.sleep_time)

    @swagger_auto_schema(
        request_body=no_body,
        responses={status.HTTP_201_CREATED: openapi.Response("Return static response", ProviderSerializer)},
    )
    def post(self, request, *args, **kwargs):
        json_file_path = self._get_json_file()
        response_json = self._get_json_response(json_file_path=json_file_path)
        self._sleep_time()
        return Response(response_json, status=status.HTTP_201_CREATED)


class ProviderAListAPIView(GenericProviderCreateAPIView):
    json_file_path = "src/apps/flights/helper_data/response_a.json"


class ProviderBListAPIView(GenericProviderCreateAPIView):
    json_file_path = "src/apps/flights/helper_data/response_b.json"
    sleep_time = 60
