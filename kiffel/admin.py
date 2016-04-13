from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats

from kiffel.models import Person
from kiffel.resources import KiffelResource
from kiffel.admin_actions import renew_kdv_barcode


@admin.register(Person)
class KiffelAdmin(ImportExportMixin, admin.ModelAdmin):
    # admin list table view
    list_display = ['nickname', 'vorname', 'nachname', 'student', 'datum_bezahlt',
        'datum_tshirt_erhalten', 'kdv_id', 'ist_orga']
    list_display_links = ['nickname']
    list_filter = ['status', 'ist_orga', 'student', 'datum_bezahlt', 'datum_teilnahmebestaetigung_erhalten']
    actions = [renew_kdv_barcode,]

    # import format options
    formats = (base_formats.CSV,)
    resource_class = KiffelResource
