from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


class Booking(models.Model):
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Номер",
    )
    date_start = models.DateField(verbose_name="Дата заезда")
    date_end = models.DateField(verbose_name="Дата выезда")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "bookings"
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["date_start"]

    def __str__(self):
        return f"Бронь {self.id}: Номер {self.room.id} с {self.date_start} по {self.date_end}"

    def clean(self):
        errors = []

        if self.date_start and self.date_end:
            if self.date_start >= self.date_end:
                errors.append("Дата окончания должна быть позже даты начала")

            if self.date_start < date.today():
                errors.append("Нельзя бронировать на прошедшие даты")

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def check_availability(self):
        overlapping_bookings = Booking.objects.filter(
            room=self.room, date_start__lt=self.date_end, date_end__gt=self.date_start
        )

        if self.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

        return not overlapping_bookings.exists()

    def get_duration_days(self):
        return (self.date_end - self.date_start).days
