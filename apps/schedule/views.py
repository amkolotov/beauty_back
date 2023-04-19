from django.shortcuts import render


def schedule(request):
    context = {}
    return render(request, 'schedule/schedule.html', context)
