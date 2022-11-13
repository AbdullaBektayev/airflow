from rest_framework import serializers

from src.apps.flights.models import AirflowSearch, Ticket
from src.settings import DEFAULT_DECIMAL_PLACES, DEFAULT_MAX_DIGITS


class AirflowSearchCreateSerializer(serializers.ModelSerializer):
    search_id = serializers.UUIDField(source="uuid")

    class Meta:
        model = AirflowSearch
        fields = ("search_id",)


class PricingForTicketSerializer(serializers.Serializer):
    base_price = serializers.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    tax_price = serializers.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    total_price = serializers.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    currency = serializers.CharField(source="currency.title")

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class PriceForTicketSerializer(serializers.Serializer):
    converted_price = serializers.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    converted_currency = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TicketForAirflowSearchSerializer(serializers.ModelSerializer):
    pricing = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    @staticmethod
    def get_pricing(ticket):
        serializer = PricingForTicketSerializer(ticket)
        return serializer.data

    @staticmethod
    def get_price(ticket):
        serializer = PriceForTicketSerializer(ticket)
        return serializer.data

    class Meta:
        model = Ticket
        fields = ("uuid", "pricing", "price")


class AirflowSearchRetrieveSerializer(serializers.ModelSerializer):
    tickets = TicketForAirflowSearchSerializer(many=True, read_only=True)

    class Meta:
        model = AirflowSearch
        fields = ("uuid", "tickets", "state")
