from django.contrib import admin
from .models import Room, Booking


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Админ-панель для номеров"""
    list_display = ('id', 'description', 'price_per_night', 'created_at', 'bookings_count')
    list_filter = ('created_at', 'price_per_night')
    search_fields = ('description',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def bookings_count(self, obj):
        """Количество бронирований номера"""
        return obj.bookings.count()
    bookings_count.short_description = 'Количество бронирований'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Админ-панель для бронирований"""
    list_display = ('id', 'room', 'date_start', 'date_end', 'created_at', 'duration_days')
    list_filter = ('date_start', 'date_end', 'created_at', 'room')
    search_fields = ('room__description',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def duration_days(self, obj):
        """Продолжительность бронирования в днях"""
        return (obj.date_end - obj.date_start).days
    duration_days.short_description = 'Дней'