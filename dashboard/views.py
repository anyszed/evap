import calendar as cal_module
from datetime import date

from django.db.models import Count, Q
from django.shortcuts import render

from planner.models import Project, Task
from notes.models import Note
from calendar_app.models import Event


def home(request):
    today = date.today()

    # -------------------------
    # NOTES (dernières, réellement visibles - is_deleted manquait avant)
    # -------------------------
    notes = Note.objects.filter(is_deleted=False).order_by('-is_pinned', 'position')[:3]

    # -------------------------
    # PROJET VEDETTE (classeur) - le plus proche de son échéance
    # -------------------------
    featured_project = Project.objects.filter(done=False).annotate(
        total_tasks=Count("task", distinct=True),
        done_tasks=Count("task", filter=Q(task__done=True), distinct=True),
    ).order_by('due_date').first()

    if featured_project:
        featured_project.percent = round(
            featured_project.done_tasks / featured_project.total_tasks * 100
        ) if featured_project.total_tasks else 0

    # -------------------------
    # CALENDRIER (mini-grille du mois en cours)
    # -------------------------
    cal_module.setfirstweekday(cal_module.MONDAY)
    month_weeks = cal_module.monthcalendar(today.year, today.month)

    event_days = set(
        Event.objects.filter(
            start__year=today.year, start__month=today.month
        ).values_list('start__day', flat=True)
    )

    today_events = Event.objects.filter(start__date=today).order_by('start')

    # -------------------------
    # TÂCHES DUES AUJOURD'HUI (pense-bête d'en-tête)
    # -------------------------
    tasks_today_count = Task.objects.filter(done=False, due_date=today).count()

    return render(request, "dashboard/home.html", {
        "notes": notes,
        "featured_project": featured_project,
        "month_weeks": month_weeks,
        "event_days": event_days,
        "today_events": today_events,
        "today": today,
        "tasks_today_count": tasks_today_count,
    })
