from django.contrib import admin  # noqa: F401

from src.apps.flights.models import AirflowSearch, Currency, Provider, Ticket


# Register your models here.


@admin.register(AirflowSearch)
class AirflowSearchAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketSearchAdmin(admin.ModelAdmin):
    pass
