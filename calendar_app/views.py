import json
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime, parse_date
from .models import Event


def calendar_page(request):
    return render(request, "calendar_app/calendar.html")


def get_events(request):
    events = Event.objects.all()

    result = []

    for e in events:

        result.append({
            "id": e.id,
            "title": e.title,
            "start": e.start.isoformat(),
            "end": e.end.isoformat() if e.end else None,
            "color": e.color,
        })

        # 🔥 RECURRENCE EXPANSION
        if hasattr(e, "recurrence_type") and e.recurrence_type and e.recurrence_end:

            current = e.start

            for i in range(1, 52):  # 1 an max sécurité

                if e.recurrence_type == "weekly":
                    current = e.start + timedelta(weeks=i)

                elif e.recurrence_type == "daily":
                    current = e.start + timedelta(days=i)

                elif e.recurrence_type == "monthly":
                    try:
                        current = e.start.replace(month=e.start.month + i)
                    except:
                        break

                if current.date() > e.recurrence_end:
                    break

                result.append({
                    "id": f"{e.id}-r{i}",
                    "title": e.title,
                    "start": current.isoformat(),
                    "end": (current + (e.end - e.start)).isoformat() if e.end else None,
                    "color": e.color,
                })

    return JsonResponse(result, safe=False)


def create_event(request):
    if request.method == "POST":
        data = json.loads(request.body)

        start = parse_datetime(data["start"])
        end = parse_datetime(data["end"]) if data.get("end") else None

        event = Event.objects.create(
            title=data["title"],
            start=start,
            end=end,
            color=data.get("color", "#F472B6"),
            recurrence_type=data.get("recurrence_type"),
            recurrence_end=parse_date(data.get("recurrence_end")) if data.get("recurrence_end") else None
        )

        return JsonResponse({"id": event.id})


def update_event(request, event_id):
    if request.method == "POST":
        data = json.loads(request.body)

        event = Event.objects.get(id=event_id)

        event.start = parse_datetime(data["start"])
        event.end = parse_datetime(data["end"]) if data.get("end") else None

        event.save()

        return JsonResponse({"status": "updated"})