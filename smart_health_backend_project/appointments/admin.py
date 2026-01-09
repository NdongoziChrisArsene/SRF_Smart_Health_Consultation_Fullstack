from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "doctor",
        "date",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "date",
        "created_at",
    )

    search_fields = (
        "patient__user__username",
        "doctor__user__username",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)
