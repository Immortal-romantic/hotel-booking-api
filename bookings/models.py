from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Booking(models.Model):
    """Модель бронирования номера"""
    room = models.ForeignKey(
        'rooms.Room',  # Ссылка на модель Room из другого приложения
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Номер"
    )
    date_start = models.DateField(verbose_name="Дата заезда")
    date_end = models.DateField(verbose_name="Дата выезда")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        db_table = 'bookings'
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['date_start']  # Сортировка по дате начала
    
    def __str__(self):
        return f"Бронь {self.id}: Номер {self.room.id} с {self.date_start} по {self.date_end}"
    
    def clean(self):
        """Валидация данных бронирования"""
        errors = []
        
        if self.date_start and self.date_end:
            # Дата окончания должна быть после даты начала
            if self.date_start >= self.date_end:
                errors.append("Дата окончания должна быть позже даты начала")
            
            # Нельзя бронировать на прошедшие даты
            if self.date_start < date.today():
                errors.append("Нельзя бронировать на прошедшие даты")
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        """Сохранение с валидацией"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def check_availability(self):
        """
        Проверка доступности номера на выбранные даты
        Возвращает True если номер свободен, False если занят
        """
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            date_start__lt=self.date_end,
            date_end__gt=self.date_start
        )
        
        # При обновлении исключаем текущее бронирование
        if self.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)
        
        return not overlapping_bookings.exists()
    
    def get_duration_days(self):
        """Количество дней бронирования"""
        return (self.date_end - self.date_start).days