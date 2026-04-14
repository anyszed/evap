import json
import random

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Note


PASTEL_COLORS = [
    "bg-pink-100",
    "bg-pink-200",
    "bg-rose-100",
    "bg-fuchsia-100",
    "bg-purple-100",
]


def notes_home(request):
    notes = Note.objects.filter(is_deleted=False).order_by("position")
    return render(request, "notes/home.html", {"notes": notes})


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    return JsonResponse({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "is_pinned": note.is_pinned
    })


@csrf_exempt
def create_note(request):
    data = json.loads(request.body)

    note = Note.objects.create(
        title=data.get("title") or "Sans titre",
        content=data.get("content") or "",
        color=random.choice(PASTEL_COLORS)
    )

    return JsonResponse({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "color": note.color,
        "is_pinned": note.is_pinned
    })


@csrf_exempt
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.is_deleted = True
    note.save()

    return JsonResponse({"status": "deleted"})


@csrf_exempt
def toggle_pin(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.is_pinned = not note.is_pinned
    note.save()

    return JsonResponse({
        "status": "ok",
        "pinned": note.is_pinned
    })

@csrf_exempt
def reorder_notes(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order = data.get("order", [])

        for item in order:
            try:
                note = Note.objects.get(id=item["id"])
                note.position = item["position"]
                note.save()
            except Note.DoesNotExist:
                pass

        return JsonResponse({"status": "ok"})

def update_note(request, note_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            note = Note.objects.get(id=note_id)

            note.title = data.get("title", "")
            note.content = data.get("content", "")

            note.save()

            return JsonResponse({"status": "ok"})

        except Note.DoesNotExist:
            return JsonResponse({"error": "not found"}, status=404)

    return JsonResponse({"error": "invalid method"}, status=400)

def get_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id)

        return JsonResponse({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "is_pinned": note.is_pinned,
        })

    except Note.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)
    
