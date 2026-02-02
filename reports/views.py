import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from django.db.models import Count, Q  # Q est essentiel pour la recherche multi-critères
from django.db import models
from xhtml2pdf import pisa

# Importations locales
from .models import FieldReport
from .utils import transcribe_audio
from django.conf import settings

# --- DÉCORATEUR DE SÉCURITÉ ---
def group_required(group_name):
    """Vérifie si l'utilisateur est dans le groupe. Sinon, redirection vers le dashboard agent."""
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser or request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Accès réservé aux Coordinateurs.")
                return redirect('dashboard')
        return _wrapped_view
    return decorator

# --- VUE : DASHBOARD AGENT (SAISIE) ---
@login_required
def dashboard(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        sector = request.POST.get('sector')
        audio_file = request.FILES.get('audio')
        is_urgent = 'is_urgent' in request.POST 

        if audio_file:
            report = FieldReport.objects.create(
                agent=request.user,
                location_detail=location,
                sector=sector,
                voice_file=audio_file,
                is_urgent=is_urgent
            )

            try:
                text = transcribe_audio(report.voice_file.name)
                report.transcription = text
                report.save()
                messages.success(request, "Rapport envoyé et analysé par l'IA !")
            except Exception as e:
                messages.error(request, f"Erreur de transcription : {e}")
        else:
            messages.error(request, "Veuillez joindre un fichier audio.")
        
        return redirect('dashboard')

    # Un agent ne voit que son propre travail
    reports = FieldReport.objects.filter(agent=request.user).order_by('-created_at')
    return render(request, 'reports/dashboard.html', {'reports': reports})

# --- VUE : SUPPRESSION ---
@login_required
def delete_report(request, report_id):
    report = get_object_or_404(FieldReport, id=report_id, agent=request.user)
    report.delete()
    messages.success(request, "Rapport supprimé.")
    return redirect('dashboard')

# --- VUE : DASHBOARD SUPERVISEUR (AVEC FILTRES) ---
@login_required
@group_required('Coordinateurs')
def supervisor_dashboard(request):
    # 1. Base de données complète
    all_reports = FieldReport.objects.all().order_by('-created_at')

    # 2. Récupération des filtres depuis l'URL
    query = request.GET.get('q')
    sector_filter = request.GET.get('sector')
    urgent_only = request.GET.get('urgent')

    # 3. Application dynamique des filtres
    if query:
        # Recherche dans la transcription OU la localité (insensible à la casse)
        all_reports = all_reports.filter(
            Q(transcription__icontains=query) | Q(location_detail__icontains=query)
        )
    
    if sector_filter:
        all_reports = all_reports.filter(sector=sector_filter)
        
    if urgent_only:
        all_reports = all_reports.filter(is_urgent=True)

    # 4. Calcul des statistiques sur les résultats filtrés
    total_count = all_reports.count()
    urgent_count = all_reports.filter(is_urgent=True).count()
    sector_stats = all_reports.values('sector').annotate(total=Count('sector'))

    context = {
        'reports': all_reports,
        'total_count': total_count,
        'urgent_count': urgent_count,
        'sector_stats': sector_stats,
    }
    # Préparation des données pour le graphique par secteur
    # On extrait les noms des secteurs et le nombre de rapports pour chacun
    labels = [stat['sector'] for stat in sector_stats]
    data = [stat['total'] for stat in sector_stats]

    context = {
        'reports': all_reports,
        'total_count': total_count,
        'urgent_count': urgent_count,
        'sector_stats': sector_stats,
        'labels': labels,  # Ajout pour le graphique
        'data': data,      # Ajout pour le graphique
    }
    return render(request, 'reports/supervisor.html', context)

# --- VUE : EXPORT PDF ---
@login_required
@group_required('Coordinateurs')
def export_pdf_report(request):
    # On peut aussi appliquer les filtres ici si on veut un PDF filtré, 
    # mais par défaut, on exporte tout le flux actuel.
    reports = FieldReport.objects.all().order_by('-created_at')
    
    template_path = 'reports/pdf_report.html'
    context = {
        'reports': reports,
        'total_count': reports.count(),
        'urgent_count': reports.filter(is_urgent=True).count(),
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Rapport_MEAL_Export.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
       return HttpResponse('Erreur lors de la génération PDF', status=500)
    return response

from django.template.loader import render_to_string
from xhtml2pdf import pisa # Assure-toi d'avoir fait : pip install xhtml2pdf

@login_required
@group_required('Coordinateurs')
def export_pdf(request):
    reports = FieldReport.objects.all().order_by('-created_at')
    html = render_to_string('reports/pdf_report.html', {'reports': reports})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_meal.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response

# Ajoute aussi cette vue pour la suppression (utilisée dans ton dashboard)
@login_required
def delete_report(request, report_id):
    report = get_object_or_404(FieldReport, id=report_id, agent=request.user)
    report.delete()
    messages.success(request, "Rapport supprimé avec succès.")
    return redirect('dashboard')

from django.template.loader import render_to_string
from xhtml2pdf import pisa 

@login_required
def export_pdf(request):
    reports = FieldReport.objects.all().order_by('-created_at')
    html = render_to_string('reports/pdf_report.html', {'reports': reports})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_meal.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response