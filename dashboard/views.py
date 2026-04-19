from django.shortcuts import render
from datetime import datetime, timedelta

from planner.models import Task
from notes.models import Note
from calendar_app.models import Event  # 🔥 IMPORTANT


def home(request):

    today = datetime.today()
    start_week = today - timedelta(days=today.weekday())

    # -------------------------
    # WEEK DAYS
    # -------------------------
    week_days = []
    for i in range(7):
        d = start_week + timedelta(days=i)
        week_days.append({
            "name": d.strftime("%a"),
            "date": d.date()
        })

    # -------------------------
    # HOURS
    # -------------------------
    hours = list(range(8, 20))

    # -------------------------
    # EVENTS (🔥 ICI LE FIX)
    # -------------------------
    events = Event.objects.filter(
        start__date__gte=start_week.date(),
        start__date__lte=(start_week + timedelta(days=6)).date()
    )

    # -------------------------
    # TASKS
    # -------------------------
    tasks_priority = Task.objects.filter(priority=3)

    # -------------------------
    # NOTES
    # -------------------------
    notes = Note.objects.all().order_by('position')[:5]

    # -------------------------
    # STATS
    # -------------------------
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(done=True).count()

    percent = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    stats = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "total_notes": Note.objects.count(),
        "percent": percent
    }

    return render(request, "dashboard/home.html", {
        "week_days": week_days,
        "hours": hours,
        "events": events,  # 🔥 IMPORTANT
        "tasks_priority": tasks_priority,
        "notes": notes,
        "stats": stats
    })