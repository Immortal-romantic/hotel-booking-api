from django.db import models

# class Room(models.Model):
#     """Модель номера отеля"""
#     description = models.TextField(verbose_name="Описание номера")
#     price_per_night = models.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         verbose_name="Цена за ночь"
#     )
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
 
 
class Room(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.pk}: {self.description[:50]}"

    
    class Meta:
        db_table = 'rooms'
        verbose_name = 'Номер отеля'
        verbose_name_plural = 'Номера отелей'
        ordering = ['-created_at']  # По умолчанию сортировка по дате создания (новые первые)
        
    
    def get_bookings_count(self):
        """Количество бронирований этого номера"""
        return self.bookings.count()
    
    def is_available(self, date_start, date_end):
        """Проверка доступности номера на указанные даты"""
        from bookings.models import Booking
        
        overlapping_bookings = Booking.objects.filter(
            room=self,
            date_start__lt=date_end,
            date_end__gt=date_start
        )
        return not overlapping_bookings.exists()