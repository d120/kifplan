from django.contrib import admin

from aks.models import AK

@admin.register(AK)
class AKAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['titel', 'leiter', 'anzahl', 'wann', 'dauer']
    list_display_links = ['titel']
