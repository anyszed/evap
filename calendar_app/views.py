import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Event


# PAGE CALENDAR
def calendar_page(request):
    return render(request, "calendar_app/calendar.html")


# GET EVENTS
def get_events(request):
    events = Event.objects.all()

    data = [
        {
            "id": e.id,
            "title": e.title,
            "start": e.start.isoformat(),
            "end": e.end.isoformat() if e.end else None,
            "color": e.color,
        }
        for e in events
    ]

    return JsonResponse(data, safe=False)


# CREATE EVENT
def create_event(request):
    if request.method == "POST":
        data = json.loads(request.body)

        event = Event.objects.create(
            title=data["title"],
            start=data["start"],
            end=data.get("end"),
            color=data.get("color", "#F472B6")
        )

        return JsonResponse({"id": event.id})


# UPDATE EVENT (drag / resize)
def update_event(request, event_id):
    if request.method == "POST":
        data = json.loads(request.body)

        event = Event.objects.get(id=event_id)
        event.start = data["start"]
        event.end = data.get("end")
        event.save()

        return JsonResponse({"status": "updated"})