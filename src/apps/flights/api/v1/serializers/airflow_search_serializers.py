from rest_framework import serializers

from apps.flights.models import AirflowSearch
from settings import DEFAULT_MAX_DIGITS, DEFAULT_DECIMAL_PLACES


class AirflowSearchCreateSerializer(serializers.ModelSerializer):
    search_id = serializers.UUIDField(source='uuid')

    class Meta:
        model = AirflowSearch
        fields = (
            "search_id",
        )


class PricingForFlightSerializer(serializers.Serializer):
    base_price = serializers.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    tax_price = serializers.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    total_price = serializers.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    currency = serializers.CharField(source='currency__title')

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class PriceForFlightSerializer(serializers.Serializer):
    converted_price = serializers.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    converted_currency = serializers.CharField(source='currency__title')

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class FlightForAirflowSearchSerializer(serializers.Serializer):
    pricing = PricingForFlightSerializer()
    price = PriceForFlightSerializer()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class AirflowSearchRetrieveSerializer(serializers.ModelSerializer):
    search_id = serializers.UUIDField(source='uuid', read_only=True)
    flights = FlightForAirflowSearchSerializer(many=True, read_only=True)

    class Meta:
        model = AirflowSearch
        fields = (
            "search_id",
            "flights",
            "state"
        )
