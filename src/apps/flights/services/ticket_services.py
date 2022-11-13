from django.db.models import CharField, F, QuerySet, Value


class TicketPriceConvertor:
    @staticmethod
    def _get_annotated_values(currency) -> dict:

        return {
            "total_price": F("base_price") + F("tax_price"),
            "converted_price": (F("total_price") * F("currency__in_kzt")) / currency.in_kzt,
            "converted_currency": Value(currency.title, CharField()),
        }

    @classmethod
    def get_queryset_with_calculation(cls, queryset, currency) -> QuerySet:

        return queryset.annotate(**cls._get_annotated_values(currency=currency)).order_by(
            "converted_price",
        )
