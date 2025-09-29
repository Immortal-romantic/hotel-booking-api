from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
        "price_display",
        "created_at",
        "bookings_count",
    )
    list_filter = ("created_at",)
    search_fields = ("description",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def bookings_count(self, obj):
        return obj.bookings.count()

    bookings_count.short_description = "Количество бронирований"

    def price_display(self, obj):
        if hasattr(obj, "price"):
            return obj.price
        if hasattr(obj, "price_per_night"):
            return obj.price_per_night
        return None

    price_display.short_description = "Цена за ночь"
    price_display.admin_order_field = "price"
