import datetime

from django.db.models import Prefetch
from django.http import HttpResponseNotFound
from django.shortcuts import render

from apps.salon.models import Specialist, Order, Salon
from apps.schedule.models import PlannedSegment
from apps.schedule.services import get_range_for_segments, get_default_time_start, get_default_time_end


def schedule_salon(request):
    context = {}
    salon_id = request.GET.get('salon')

    try:
        date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d").date()
    except Exception:
        date = None

    salon = Salon.objects.filter(id=salon_id).first()
    if not salon or not date or not request.user.is_staff:
        return HttpResponseNotFound("Page not found")

    context['specialists'] = Specialist.objects.filter(salons=salon_id).prefetch_related(
                        Prefetch(
                            'spec_segments',
                            queryset=PlannedSegment.objects.filter(
                                date=date, segment__start_time__gte=get_default_time_start(),
                                segment__end_time__lte=get_default_time_end()
                            ).select_related('segment', 'order').order_by('segment__number')
                        )
    )
    context['range'], context['range_titles'] = get_range_for_segments()
    context['date'] = date
    context['salon_name'] = salon.name
    return render(request, 'schedule/schedule_salon.html', context)


def schedule_spec(request, pk):

    if not Specialist.objects.filter(id=pk).exists():
        return HttpResponseNotFound("Page not found")

    context = {}
    date_from = datetime.datetime.today().date()
    date_to = (datetime.datetime.today() + datetime.timedelta(days=28)).date()
    context['spec'] = Specialist.objects.filter(id=pk).prefetch_related(
                        Prefetch(
                            'spec_segments',
                            queryset=PlannedSegment.objects.filter(
                                date__gte=date_from, date__lte=date_to
                            ).select_related('segment', 'order').order_by('date', 'segment__number')
                        )
    ).first()
    context['range'], context['range_titles'] = get_range_for_segments()
    context['range_date'] = [(datetime.datetime.today() + datetime.timedelta(days=i)).date() for i in range(28)]

    return render(request, 'schedule/schedule_spec.html', context)
