from django.shortcuts import render


def schedule_salon(request):
    context = {}
    return render(request, 'schedule/schedule_salon.html', context)


def schedule_spec(request):
    context = {}
    return render(request, 'schedule/schedule_spec.html', context)
