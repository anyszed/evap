import json
import uuid
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime, parse_date

from .models import Event


# ---------------- PAGE ----------------
def calendar_page(request):
    return render(request, "calendar_app/calendar.html")


# ---------------- GET EVENTS ----------------
def get_events(request):
    events = Event.objects.all()

    return JsonResponse([
        {
            "id": e.id,
            "title": e.title,
            "start": e.start.isoformat(),
            "end": e.end.isoformat() if e.end else None,
            "color": e.color,
            "series_id": str(e.series_id) if e.series_id else None
        }
        for e in events
    ], safe=False)


# ---------------- CREATE ----------------
def create_event(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)

    start = parse_datetime(data.get("start"))
    end = parse_datetime(data.get("end")) if data.get("end") else None

    if not start:
        return JsonResponse({"error": "invalid start"}, status=400)

    recurrence_type = data.get("recurrence_type")
    recurrence_end = parse_date(data.get("recurrence_end")) if data.get("recurrence_end") else None

    series_id = str(uuid.uuid4()) if recurrence_type else None

    base_event = Event.objects.create(
        title=data["title"],
        start=start,
        end=end,
        color=data.get("color", "#F472B6"),
        recurrence_type=recurrence_type,
        recurrence_end=recurrence_end,
        series_id=series_id
    )

    # ---------------- RECURRING ----------------
    if recurrence_type and recurrence_end:

        delta = None
        if recurrence_type == "daily":
            delta = timedelta(days=1)
        elif recurrence_type == "weekly":
            delta = timedelta(weeks=1)
        elif recurrence_type == "monthly":
            delta = timedelta(days=30)

        if delta:
            i = 1
            while True:
                next_start = start + delta * i

                if next_start.date() > recurrence_end:
                    break

                Event.objects.create(
                    title=data["title"],
                    start=next_start,
                    end=(end + delta * i) if end else None,
                    color=base_event.color,
                    recurrence_type=recurrence_type,
                    recurrence_end=recurrence_end,
                    series_id=series_id
                )

                i += 1

    return JsonResponse({
        "id": base_event.id,
        "series_id": series_id
    })


# ---------------- UPDATE ----------------
def update_event(request, event_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    mode = data.get("mode", "single")

    # ---------------- SINGLE ----------------
    if mode == "single":
        event.start = parse_datetime(data["start"])
        event.end = parse_datetime(data["end"]) if data.get("end") else None
        event.save()
        return JsonResponse({"status": "updated single"})

    # ---------------- SERIES ----------------
    if mode == "series":

        if not event.series_id:
            return JsonResponse({"error": "no series"}, status=400)

        events = Event.objects.filter(series_id=event.series_id)

        base_start = parse_datetime(data["start"])
        if not base_start:
            return JsonResponse({"error": "invalid start"}, status=400)

        offset = base_start - event.start

        for e in events:
            e.start = e.start + offset
            e.end = (e.end + offset) if e.end else None
            e.save()

        return JsonResponse({"status": "updated series"})

    return JsonResponse({"error": "invalid mode"}, status=400)


# ---------------- DELETE ----------------
def delete_event(request, event_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    mode = data.get("mode", "single")

    # ---------------- SINGLE ----------------
    if mode == "single":
        event.delete()
        return JsonResponse({"status": "deleted single"})

    # ---------------- SERIES ----------------
    if mode == "series":
        if not event.series_id:
            return JsonResponse({"error": "no series"}, status=400)

        Event.objects.filter(series_id=event.series_id).delete()
        return JsonResponse({"status": "deleted series"})

    return JsonResponse({"error": "invalid mode"}, status=400)