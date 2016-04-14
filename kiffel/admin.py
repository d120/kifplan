from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats

from kiffel.models import Person
from kiffel.resources import KiffelResource
from kiffel.admin_actions import renew_kdv_barcode

from django.contrib.auth.forms import UserChangeForm



@admin.register(Person)
class KiffelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Override this to set the password to the value in the field if it's
        # changed.
        if obj.pk:
            orig_obj = Person.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()
    
    # admin list table view
    list_display = ['nickname', 'vorname', 'nachname', 'ist_helfer', 'ist_orga', 'ist_kiffel',
        'datum_tshirt_erhalten', 'kdv_id',  'engel_id', 'anmeldung_id']
    list_display_links = ['nickname']
    list_filter = ['status', 'ist_orga', 'student', 'datum_bezahlt', 'datum_teilnahmebestaetigung_erhalten']
    actions = [renew_kdv_barcode,]

    # import format options
    formats = (base_formats.CSV,)
    resource_class = KiffelResource
