from django.contrib import admin
from .models import FieldReport

@admin.register(FieldReport)
class FieldReportAdmin(admin.ModelAdmin):
    # On retire 'organization' car il n'existe pas dans ton models.py
    list_display = ('location_detail', 'sector', 'is_urgent', 'created_at')
    list_filter = ('sector', 'is_urgent')
    search_fields = ('location_detail', 'transcription')