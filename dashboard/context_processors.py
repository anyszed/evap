from datetime import date

from notes.models import Note
from planner.models import Project
from grades.models import GradeTable


def binder_bar(request):
    """
    Données légères pour la barre "classeur" (nav globale, templates/base.html)
    qui remplace l'ancienne sidebar. Un contexte processor plutôt que de
    dupliquer ces requêtes dans chaque vue (notes/planner/calendar/timer/
    grades) : la barre est dans {% block chrome %}, donc partagée par
    toutes les pages sauf le tableau de bord (qui garde sa propre nav via
    les 5 objets du bureau, cf. Passe 4).
    """
    notes_count = Note.objects.filter(is_deleted=False).count()
    active_projects_count = Project.objects.filter(done=False).count()

    grades_average = None
    table = GradeTable.objects.prefetch_related('subjects__grades').first()
    if table:
        total, total_coeff = 0.0, 0.0
        for subject in table.subjects.all():
            grades = list(subject.grades.all())
            s_total = sum(g.value * g.coefficient for g in grades)
            s_coeff = sum(g.coefficient for g in grades)
            subject_avg = (s_total / s_coeff) if s_coeff else 0
            total += subject_avg * subject.coefficient
            total_coeff += subject.coefficient
        if total_coeff:
            grades_average = round(total / total_coeff, 1)

    return {
        "binder_notes_count": notes_count,
        "binder_active_projects_count": active_projects_count,
        "binder_today": date.today(),
        "binder_grades_average": grades_average,
    }
