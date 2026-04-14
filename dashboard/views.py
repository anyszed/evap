from django.shortcuts import render
from .models import Note

def home(request):
    notes = Note.objects.all().order_by('-created_at')
    context = {
        'notes': notes
    }
    return render(request, 'dashboard/home.html', context)