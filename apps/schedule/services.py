import datetime

from apps.salon.models import CompanyInfo


def get_default_time_start():
    """Возвращает время начала работы компании"""
    return CompanyInfo.objects.first().work_time_start or datetime.time(10, 0)


def get_default_time_end():
    """Возвращает время окончания работы компании"""
    return CompanyInfo.objects.first().work_time_end or datetime.time(20, 0)


def get_range_for_segments():
    """Возвращает диапазон номеров и заголовков временных интервалов"""
    from apps.schedule.models import Segment
    segments = Segment.objects.filter(
        start_time__gte=get_default_time_start(), end_time__lte=get_default_time_end()
    ).exclude(start_time__gt=get_default_time_end()).order_by('number')
    range_numbers = range(segments.first().number, segments.last().number + 1)
    range_titles = (f'{segment.start_time.strftime("%H:%M")}-{segment.end_time.strftime("%H:%M")}'
                    for segment in segments)
    return range_numbers, range_titles
