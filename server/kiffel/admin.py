from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats
from import_export.widgets import DateWidget, BooleanWidget, Widget

from kiffel.models import Kiffel

class JaNeinBooleanWidget(Widget):
    def clean(value):
        return True if value == "Ja" else False
    def render(value):
        return "Ja" if value else "Nein"


class KiffelResource(resources.ModelResource):
    vorname = fields.Field(attribute='vorname', column_name='Vorname')
    nachname = fields.Field(attribute='nachname', column_name='Nachname')
    email = fields.Field(attribute='email', column_name='E-Mail')
    nickname = fields.Field(attribute='nickname', column_name='Namensschildername')
    student = fields.Field(attribute='student', column_name='Student', widget=JaNeinBooleanWidget, default=False)
    hochschule = fields.Field(attribute='hochschule', column_name='Hochschule/Ort/Verein')
    kommentar_public = fields.Field(attribute='kommentar_public', column_name='Öffentlicher Kommentar')
    kommentar_orga = fields.Field(attribute='kommentar_orga', column_name='Kommentar für Orgas')
    anreise_geplant = fields.Field(attribute='anreise_geplant', column_name='Anreise',
        widget=DateWidget(format='%d.%m.%Y'))
    abreise_geplant = fields.Field(attribute='abreise_geplant', column_name='Abreise',
        widget=DateWidget(format='%d.%m.%Y'))
    ernaehrungsgewohnheit = fields.Field(attribute='ernaehrungsgewohnheit', column_name='Ernährungsgewohnheit')
    lebensmittelunvertraeglichkeiten = fields.Field(attribute='lebensmittelunvertraeglichkeiten',
        column_name='Lebensmittelunverträglichkeiten etc.')
    volljaehrig = fields.Field(attribute='volljaehrig', column_name='Über 18',
        widget=JaNeinBooleanWidget, default=False)
    eigener_schlafplatz = fields.Field(attribute='eigener_schlafplatz', column_name='Habe eigenen Schlafplatz',
        widget=JaNeinBooleanWidget, default=False)
    tshirt_groesse = fields.Field(attribute='tshirt_groesse', column_name='T-Shirt-Größe')
    nickname_auf_tshirt = fields.Field(attribute='nickname_auf_tshirt',
        column_name='Namensschildername auf T-Shirt (+5€)',
        widget=JaNeinBooleanWidget, default=False)
    kapuzenjacke_groesse = fields.Field(attribute='kapuzenjacke_groesse', column_name='Kapuzenjacke (25€)')
    nickname_auf_kapuzenjacke = fields.Field(attribute='nickname_auf_kapuzenjacke',
        column_name='Namensschildername auf Kapuzenjacke (+5€)',
        widget=JaNeinBooleanWidget, default=False)
    weitere_tshirts = fields.Field(attribute='weitere_tshirts', column_name='zusätzliche T-Shirts (in gleicher Größe)')
    interesse_theater = fields.Field(attribute='interesse_theater', column_name='Interesse an Theaterbesuch',
        widget=JaNeinBooleanWidget, default=False)
    interesse_esoc = fields.Field(attribute='interesse_esoc', column_name='Interesse an ESOC Führung',
        widget=JaNeinBooleanWidget, default=False)
    anmeldung_angelegt = fields.Field(attribute='anmeldung_angelegt', column_name='Angelegt',
        widget=DateWidget(format='%Y-%m-%d %H:%M:%S %z'))
    anmeldung_aktualisiert = fields.Field(attribute='anmeldung_aktualisiert', column_name='Aktualisiert',
        widget=DateWidget(format='%Y-%m-%d %H:%M:%S %z'))

    def before_save_instance(self, instance, dry_run):
        instance.status = 'angemeldet'

    class Meta:
        model = Kiffel
        exclude = ('datum_bezahlt', 'datum_tshirt_erhalten', 'datum_teilnahmebestaetigung_erhalten',
                   'kommentar', 'engel_handle', 'twitter_handle')


@admin.register(Kiffel)
class KiffelAdmin(ImportExportMixin, admin.ModelAdmin):
    # admin list table view
    list_display = ['nickname', 'vorname', 'nachname', 'email', 'student',
                    'datum_bezahlt', 'datum_tshirt_erhalten']
    list_display_links = ['nickname']

    # import format options
    formats = (base_formats.CSV,)
    resource_class = KiffelResource
