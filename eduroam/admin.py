from django.contrib import admin

from eduroam.models import GuestAccount

@admin.register(GuestAccount)
class GuestAccountAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['login', 'vorname', 'nachname', 'vergeben', 'vergeben_am']
    list_display_links = ['login']
    list_filter = ['vergeben']
