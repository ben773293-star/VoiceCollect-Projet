from django.db import models
from django.contrib.auth.models import User

class FieldReport(models.Model):
    SECTOR_CHOICES = [
        ('Agriculture', 'Agriculture'),
        ('Elevage', 'Élevage'),
        ('Eau', 'Eau & Assainissement'),
        ('Sante', 'Santé'),
    ]

    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    location_detail = models.CharField(max_length=255)
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES)
    voice_file = models.FileField(upload_to='audios/')
    transcription = models.TextField(blank=True, null=True)
    is_urgent = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True) # Important pour la carte
    longitude = models.FloatField(null=True, blank=True) # Important pour la carte
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agent.username} - {self.location_detail}"