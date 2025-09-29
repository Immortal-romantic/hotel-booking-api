from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "room",
        "date_start",
        "date_end",
        "created_at",
        "duration_days",
    )
    list_filter = ("date_start", "date_end", "created_at", "room")
    search_fields = ("room__description",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def duration_days(self, obj):
        return (obj.date_end - obj.date_start).days

    duration_days.short_description = "Дней"
