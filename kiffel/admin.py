from django.contrib import admin
from django import forms
from django.db import models
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats
from django.contrib.admin.filters import FieldListFilter
from kiffel.models import Person
from kiffel.resources import KiffelResource
import kiffel.admin_actions

from django.contrib.auth.forms import UserChangeForm
from datetime import datetime

class DropdownDatetimeWidget(forms.Select):
    def __init__(self, attrs=None):
        choices = (
            ('', 'Nein'),
            ('Now', 'Ja - jetzt'),
            ('Keep', 'Ja - Wert beibehalten'),
        )
        super(DropdownDatetimeWidget, self).__init__(attrs, choices)
    def render(self, name, value, attrs=None):
        print("render: ",value, self.choices)
        if value == None:
            value = ''
            self.choices.pop()
        elif value != None:
            #value = 'Keep'
            self.choices[2] = (str(value), 'Ja - ' + str(value))
        print("render2: ",value, self.choices)
        return super(DropdownDatetimeWidget, self).render(name, value, attrs)
    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        print("before:",value)
        if value == 'Now': return datetime.now()
        
        print("after:",value)
        return value


class IsNullListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__isnull' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg)
        super(IsNullListFilter, self).__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, changelist):
        for lookup, title in (
                (None, 'Alle'),
                ('False', 'Ja'),
                ('True', 'Nein')):
            yield {
                'selected': self.lookup_val == lookup,
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg: lookup,
                }),
                'display': title,
            }


class KiffelAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        widgets = {
            #'datum_bezahlt': forms.TextInput(), 
            #'datum_tuete_erhalten': DropdownDatetimeWidget(), 
            #'datum_tshirt_erhalten': DropdownDatetimeWidget(), 
            #'datum_teilnahmebestaetigung_erhalten': DropdownDatetimeWidget(),
        }
        exclude = ()


@admin.register(Person)
class KiffelAdmin(admin.ModelAdmin):
    form = KiffelAdminForm
    
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
    list_display = ['nickname', 'vorname', 'nachname',
        'datemarks', 'tshirt_groesse', 'hochschule', 'status_desc', 'engel_id_link', ]
    list_display_links = ['nickname']
    list_filter = [
        'ist_kiffel', 'ist_orga', 'student', 
        ('datum_bezahlt', IsNullListFilter),
        ('datum_teilnahmebestaetigung_erhalten', IsNullListFilter),
        'hochschule', ]
    actions = [
            kiffel.admin_actions.mark_bezahlt_now,
            kiffel.admin_actions.mark_tuete_erhalten_now,
            kiffel.admin_actions.mark_tshirt_erhalten_now,
            kiffel.admin_actions.mark_teilnahmebestaetigung_erhalten_now,
            kiffel.admin_actions.generate_nametags,
            kiffel.admin_actions.generate_part_cert,
            kiffel.admin_actions.renew_kdv_barcode,
    ]
    
    def get_datemark(self, obj, icon, field_name):
        # der Event Handler hierzu ist in static/kiffel/kiffelhelper.js definiert
        val = getattr(obj, field_name)
        title = Person._meta.get_field(field_name).verbose_name
        if val != None:
            state = "datemark-yes"
            title += ": ja, am " + str(val)
        else:
            state = "datemark-no"
            title += ": nein"
        return "<span class='datemark "+state+"' title='"+title+"' data-mark-id='"+str(obj.id)+"' data-mark-field='"+field_name+"'><i class='fa fa-"+icon+"'></i></span>"
        
    
    def datemarks(self, obj):
        o = ""
        o += self.get_datemark(obj, 'money', 'datum_bezahlt')
        o += self.get_datemark(obj, 'shopping-bag', 'datum_tuete_erhalten')
        o += self.get_datemark(obj, 'user', 'datum_tshirt_erhalten')
        o += self.get_datemark(obj, 'file-text', 'datum_teilnahmebestaetigung_erhalten')
        return "<nobr>" + o + "</nobr>"
    datemarks.short_description = "stuff"
    datemarks.allow_tags = True
    
    fieldsets = (
      ('', {
          'fields': ('nickname', 'vorname', 'nachname', 'student', 'hochschule', 
            )
      }),
      ('Teilnahmestatus', {
          'classes': ('collapse',),
          'fields': (
           'kommentar', 'status', 'datum_bezahlt', 'datum_tuete_erhalten', 'datum_tshirt_erhalten', 
           'datum_teilnahmebestaetigung_erhalten', )
      }),
      ('Kleidungsstücke', {
          'classes': ('collapse',),
          'fields': ('tshirt_groesse', 'nickname_auf_tshirt', 'kapuzenjacke_groesse', 'nickname_auf_kapuzenjacke',
           'weitere_tshirts',)
      }),
      ('Details aus der Anmeldung', {
          'classes': ('collapse',),
          'fields': ('anreise_geplant', 'abreise_geplant', 'ernaehrungsgewohnheit', 'lebensmittelunvertraeglichkeiten', 'volljaehrig', 
           'eigener_schlafplatz', 'interesse_theater', 'interesse_esoc', 'kommentar_public', 'kommentar_orga',
             'anmeldung_angelegt', 'anmeldung_aktualisiert', )
      }),
      ('Login-Account', {
          'classes': ('collapse',),
          'fields': ('email', #'password', 
            'ist_kiffel', 'ist_orga', 'ist_helfer', 'ist_anonym', 'is_superuser', 
            'groups', 'user_permissions', 'last_login',)
      }),
      ('crossRef', {
          'classes': ('collapse',),
          'fields': ('engel_id', 'anmeldung_id', 'twitter_handle', 'kdv_id', )
      }),
    )
    
    
