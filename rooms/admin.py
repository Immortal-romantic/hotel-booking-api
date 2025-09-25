from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Админ-панель для номеров (устойчиво к названию поля цены)"""
    list_display = ("id", "description", "price_display", "created_at", "bookings_count")
    # list_filter требует поля модели (или кастомный фильтр). Мы оставим created_at,
    # а по цене можно фильтровать через кастомный SimpleListFilter — но пока уберём price из list_filter
    list_filter = ("created_at",)
    search_fields = ("description",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def bookings_count(self, obj):
        return obj.bookings.count()
    bookings_count.short_description = "Количество бронирований"

    def price_display(self, obj):
        # поддерживаем оба возможных названия поля
        if hasattr(obj, "price"):
            return obj.price
        if hasattr(obj, "price_per_night"):
            return getattr(obj, "price_per_night")
        return None
    price_display.short_description = "Цена за ночь"
    price_display.admin_order_field = "price"  # если поля price нет, сортировка по полю не сработает — но не упадёт

