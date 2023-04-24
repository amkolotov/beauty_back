import datetime


def get_default_time_start():
    from apps.salon.models import CompanyInfo

    """Возвращает время начала работы компании"""
    return CompanyInfo.objects.first().work_time_start or datetime.time(10, 0)


def get_default_time_end():
    from apps.salon.models import CompanyInfo

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


def get_time_choices(
        start_time=datetime.time(0, 0), end_time=datetime.time(23, 30), delta=datetime.timedelta(minutes=30)
):
    """
        Builds a choices tuple of (time object, time string) tuples
        starting at the start time specified and ending at or before
        the end time specified in increments of size delta.

        The default is to return a choices tuple for
        9am to 5pm in 15-minute increments.
    """
    time_choices = ()
    time = start_time
    while True:
        time_choices += ((time, time.strftime('%H:%M')),)
        time = (datetime.datetime.combine(datetime.date.today(), time) + delta).time()
        if time == end_time:
            time_choices += ((time, time.strftime('%H:%M')),)
            break
    return time_choices
