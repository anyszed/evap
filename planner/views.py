from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_date
from .models import Project, Task

def planner_home(request):
    projects = Project.objects.filter(done=False)
    tasks = Task.objects.filter(done=False)
    return render(request, "planner/home.html", {
        "projects": projects,
        "tasks": tasks,
    })

# API pour récupérer les détails d'une tâche
def api_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return JsonResponse({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date.isoformat() if task.due_date else ""
    })

# API pour récupérer les détails d'un projet
def api_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return JsonResponse({
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "due_date": project.due_date.isoformat() if project.due_date else ""
    })

# Créer un projet
def create_project(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date") or None
        Project.objects.create(name=name, description=description, due_date=due_date)
    return redirect("planner:planner_home")

# Créer une tâche
def create_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = int(request.POST.get("priority"))
        due_date = request.POST.get("due_date") or None
        project_id = request.POST.get("project")
        project = Project.objects.get(id=project_id) if project_id else None
        Task.objects.create(title=title, description=description, priority=priority, due_date=due_date, project=project)
    return redirect("planner:planner_home")

# Mettre à jour la date d'une tâche
@csrf_exempt
def update_task_date(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        data = json.loads(request.body)
        task.due_date = parse_date(data.get("due_date"))
        task.save()
    return HttpResponse(status=204)

# Mettre à jour la date d'un projet
@csrf_exempt
def update_project_date(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        data = json.loads(request.body)
        project.due_date = parse_date(data.get("due_date"))
        project.save()
    return HttpResponse(status=204)

# Clôturer une tâche
def close_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.done = True
    task.save()
    return redirect("planner:planner_home")

# Clôturer un projet
def close_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.done = True
    project.save()
    return redirect("planner:planner_home")