import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.auth_app.validators import validate_segment, validate_time
from apps.salon.models import CompanyInfo
from .services import get_default_time_start, get_default_time_end


class Segment(models.Model):
    """Наименьший отрезок времени равный 30 минутам"""
    number = models.IntegerField(primary_key=True, unique=True, validators=[validate_segment])
    start_time = models.TimeField('Начало промежутка', validators=[validate_time])
    end_time = models.TimeField('Окончание промежутка', validators=[validate_time])

    def save(self, *args, **kwargs):
        start_min, end_min = (0, 30) if self.number % 2 != 0 else (30, 0)
        start_hour = self.number // 2 if self.number % 2 != 0 else self.number // 2 - 1
        end_hour = start_hour if end_min else start_hour + 1
        if end_hour == 24:
            end_hour = 0
        self.start_time = datetime.time(start_hour, start_min)
        self.end_time = datetime.time(end_hour, end_min)
        super(Segment, self).save(*args, **kwargs)

    class Meta:
        ordering = ['number']
        verbose_name = 'Промежуток времени'
        verbose_name_plural = 'Промежутки времени'

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'


class PlannedSegment(models.Model):
    """Рабочий отрезок времени"""
    spec = models.ForeignKey('salon.Specialist', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Cпециалист', related_name='spec_segments')
    date = models.DateField('Дата')
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='planned_segments')
    order = models.ForeignKey('salon.Order', verbose_name='Заявка', on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='order_planned_segments')
    is_busy = models.BooleanField('Занят?', default=False)

    class Meta:
        unique_together = ['spec', 'date', 'segment']
        verbose_name = 'Рабочий интервал'
        verbose_name_plural = 'Рабочие интервалы'

    def __str__(self):
        return f'{self.spec} - {self.date} - {self.segment}'


class Schedule(models.Model):
    """Распорядок работы специалиста"""
    spec = models.ForeignKey('salon.Specialist', on_delete=models.CASCADE,
                             verbose_name='Cпециалист', related_name='schedules')
    salon = models.ForeignKey('salon.Salon', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Салон', related_name='schedules')
    date = models.DateField('Дата')
    work_time_start = models.TimeField('Начало рабочего дня', validators=[validate_time],
                                       default=get_default_time_start)
    work_time_end = models.TimeField('Окончание рабочего дня', validators=[validate_time],
                                     default=get_default_time_end)
    break_time_start = models.TimeField('Начало перерыва', null=True, blank=True, validators=[validate_time])
    break_time_end = models.TimeField('Окончание перерыва', null=True, blank=True, validators=[validate_time])

    class Meta:
        unique_together = ['spec', 'date']
        ordering = ['-date']
        verbose_name = 'Дневной график работы специалиста'
        verbose_name_plural = 'Дневные графики работы специалистов'

    def __str__(self):
        return f'{self.date} - {self.spec}'

    def clean(self):
        self.is_cleaned = True

        if not self.salon:
            raise ValidationError('Выберите салон')

        if not self.work_time_start or not self.work_time_end:
            raise ValidationError('Отсутствует время начала или окончания рабочего дня')

        if self.work_time_start > self.work_time_end:
            raise ValidationError('Время начала не может быть позже времени окончания')

        if self.work_time_start < self.salon.work_time_start or self.work_time_start > self.salon.work_time_end \
                or self.work_time_end < self.salon.work_time_start or self.work_time_end > self.salon.work_time_end:
            raise ValidationError('Время работы не совпадает с временем работы салона')

        if (self.break_time_start and not self.break_time_end) or (self.break_time_end and not self.break_time_start):
            raise ValidationError('Отсутствует время начала или окончания перерыва')

        if self.break_time_start and self.break_time_end:
            if self.break_time_start < self.work_time_start or self.break_time_start > self.work_time_end\
                    or self.break_time_start >= self.break_time_end:
                raise ValidationError('Не корректное время перерыва')
        super().clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super().save()


@receiver(post_save, sender=Schedule)
def create_segments(sender, instance, created, **kwargs):
    if created:
        for segment in Segment.objects.all():
            if instance.work_time_start <= segment.start_time < instance.work_time_end:
                if instance.break_time_start and instance.break_time_start <= segment.start_time < instance.break_time_end:
                    continue
                PlannedSegment.objects.create(segment=segment, date=instance.date, spec=instance.spec)
