import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import GradeTable, Subject, Grade


# ===================== PAGE =====================

def index(request):
    tables = GradeTable.objects.prefetch_related('subjects__grades')
    return render(request, 'grades/grades.html', {'tables': tables})


# ===================== TABLE =====================

def create_table(request):
    table = GradeTable.objects.create(name="Nouveau résultat")
    return JsonResponse({"id": table.id, "name": table.name})


def delete_table(request, table_id):
    GradeTable.objects.filter(id=table_id).delete()
    return JsonResponse({"ok": True})


def update_table(request, table_id):
    data = json.loads(request.body)
    table = GradeTable.objects.get(id=table_id)
    table.name = data.get("name", table.name)
    table.save()
    return JsonResponse({"ok": True})


# ===================== SUBJECT =====================

def add_subject(request, table_id):
    table = GradeTable.objects.get(id=table_id)

    subject = Subject.objects.create(
        table=table,
        name="Nouvelle matière",
        coefficient=1
    )

    return JsonResponse({
        "id": subject.id,
        "name": subject.name,
        "coefficient": subject.coefficient
    })


def delete_subject(request, subject_id):
    Subject.objects.filter(id=subject_id).delete()
    return JsonResponse({"ok": True})


def update_subject(request, subject_id):
    data = json.loads(request.body)
    subject = Subject.objects.get(id=subject_id)

    if "name" in data:
        subject.name = data["name"]
    if "coeff" in data:
        subject.coefficient = float(data["coeff"])

    subject.save()
    return JsonResponse({"ok": True})


# ===================== GRADE =====================

def add_grade(request, subject_id):
    subject = Subject.objects.get(id=subject_id)

    grade = Grade.objects.create(
        subject=subject,
        name="",
        value=0,
        coefficient=1
    )

    return JsonResponse({
        "id": grade.id,
        "name": grade.name,
        "value": grade.value,
        "coefficient": grade.coefficient
    })


def delete_grade(request, grade_id):
    Grade.objects.filter(id=grade_id).delete()
    return JsonResponse({"ok": True})


def update_grade(request, grade_id):
    data = json.loads(request.body)
    grade = Grade.objects.get(id=grade_id)

    if "name" in data:
        grade.name = data["name"]
    if "value" in data:
        grade.value = float(data["value"])
    if "coeff" in data:
        grade.coefficient = float(data["coeff"])

    grade.save()
    return JsonResponse({"ok": True})