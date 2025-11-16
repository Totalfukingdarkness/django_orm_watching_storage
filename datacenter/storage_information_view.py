from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration


def storage_information_view(request):
    not_leaved_visits = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []
    for visit in not_leaved_visits:
        owner_name = visit.passcard.owner_name
        entered_time = visit.entered_at
        duration = get_duration(visit)
        non_closed_visits.append({
            'who_entered': owner_name,
            'entered_at': entered_time,
            'duration': format_duration(duration),
        })

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
