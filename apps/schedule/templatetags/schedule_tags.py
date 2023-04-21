from django import template

register = template.Library()


@register.filter(name="get_segment_for_index")
def get_segment_for_index(planned_segments, index):
    return planned_segments.filter(segment__number=index).first()


@register.filter(name="filter_segments_for_date")
def filter_segments_for_date(planned_segments, date):
    return planned_segments.filter(date=date).order_by('segment__number')
