from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "age", "gender", "prediction", "confidence", "created_at")
    list_filter = ("prediction", "gender", "created_at")
    search_fields = ("name", "email", "phone", "user__username", "user__email")
    readonly_fields = ("created_at",)
