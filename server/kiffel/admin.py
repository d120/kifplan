from django.contrib import admin
from kiffel.models import Kiffel

@admin.register(Kiffel)
class KiffelAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'vorname', 'nachname', 'email', 'student', 'datum_bezahlt', 'datum_tshirt_erhalten']
    list_display_links = ['nickname']
