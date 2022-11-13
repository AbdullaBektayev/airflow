from rest_framework import serializers

from src.apps.flights.models import AirflowSearch, Flight
from src.settings import DEFAULT_MAX_DIGITS, DEFAULT_DECIMAL_PLACES


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
    currency = serializers.CharField(source='currency.title')

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class PriceForFlightSerializer(serializers.Serializer):
    converted_price = serializers.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    converted_currency = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class FlightForAirflowSearchSerializer(serializers.ModelSerializer):
    pricing = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    @staticmethod
    def get_pricing(flight):
        serializer = PricingForFlightSerializer(flight)
        return serializer.data

    @staticmethod
    def get_price(flight):
        serializer = PriceForFlightSerializer(flight)
        return serializer.data

    class Meta:
        model = Flight
        fields = (
            "uuid",
            "pricing",
            "price"
        )


class AirflowSearchRetrieveSerializer(serializers.ModelSerializer):
    flights = FlightForAirflowSearchSerializer(many=True, read_only=True)

    class Meta:
        model = AirflowSearch
        fields = (
            "uuid",
            "flights",
            "state"
        )
