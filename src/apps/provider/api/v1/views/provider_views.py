import json

from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.accounts.api.permissions import IsNotAuthenticated


class GenericProviderListAPIView(ListAPIView):
    permission_classes = [IsNotAuthenticated]
    json_file_path = None

    @staticmethod
    def _get_json_response(json_file_path):
        with open(json_file_path, mode="r") as file:
            json_data = json.load(file)
        return json_data

    def _get_json_file(self):
        if self.json_file_path is None:
            raise ValueError(
                "Doesn't have json file path"
            )
        return self.json_file_path

    def get(self, request, *args, **kwargs):
        json_file_path = self._get_json_file()
        response_json = self._get_json_response(json_file_path=json_file_path)
        return Response(response_json)


class ProviderAListAPIView(GenericProviderListAPIView):
    json_file_path = "src/apps/provider/helper_data/response_a.json"


class ProviderBListAPIView(GenericProviderListAPIView):
    json_file_path = "src/apps/provider/helper_data/response_b.json"

