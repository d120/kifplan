from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats

from kiffel.models import Kiffel

class KiffelResource(resources.ModelResource):
    vorname = fields.Field(attribute='vorname', column_name='Vorname')
    nachname = fields.Field(attribute='nachname', column_name='Nachname')
    email = fields.Field(attribute='email', column_name='E-Mail')
    nickname = fields.Field(attribute='nickname', column_name='Namensschildername')
    student = fields.Field(attribute='student', column_name='Student')
    hochschule = fields.Field(attribute='hochschule', column_name='Hochschule/Ort/Verein')
    kommentar_public = fields.Field(attribute='kommentar_public', column_name='Öffentlicher Kommentar')
    kommentar_orga = fields.Field(attribute='kommentar_orga', column_name='Kommentar für Orgas')
    anreise_geplant = fields.Field(attribute='anreise_geplant', column_name='Anreise')
    abreise_geplant = fields.Field(attribute='abreise_geplant', column_name='Abreise')
    ernaehrungsgewohnheit = fields.Field(attribute='ernaehrungsgewohnheit', column_name='Ernährungsgewohnheit')
    lebensmittelunvertraeglichkeiten = fields.Field(attribute='lebensmittelunvertraeglichkeiten', column_name='Lebensmittelunverträglichkeiten etc.')
    volljaehrig = fields.Field(attribute='volljaehrig', column_name='Über 18')
    eigener_schlafplatz = fields.Field(attribute='eigener_schlafplatz', column_name='Habe eigenen Schlafplatz')
    tshirt_groesse = fields.Field(attribute='tshirt_groesse', column_name='T-Shirt-Größe')
    nickname_auf_tshirt = fields.Field(attribute='nickname_auf_tshirt', column_name='Namensschildername auf T-Shirt (+5€)')
    kapuzenjacke = fields.Field(attribute='kapuzenjacke', column_name='Kapuzenjacke (25€)')
    nickname_auf_kapuzenjacke = fields.Field(attribute='nickname_auf_kapuzenjacke', column_name='Namensschildername auf Kapuzenjacke (+5€)')
    weitere_tshirts = fields.Field(attribute='weitere_tshirts', column_name='zusätzliche T-Shirts (in gleicher Größe)')
    interesse_theater = fields.Field(attribute='interesse_theater', column_name='Interesse an Theaterbesuch')
    interesse_esoc = fields.Field(attribute='interesse_esoc', column_name='Interesse an ESOC Führung')
    anmeldung_angelegt = fields.Field(attribute='anmeldung_angelegt', column_name='Angelegt')
    anmeldung_aktualisiert = fields.Field(attribute='anmeldung_aktualisiert', column_name='Aktualisiert')

    class Meta:
        model = Kiffel
        exclude = ('datum_bezahlt', 'datum_tshirt_erhalten', 'datum_teilnahmebestaetigung_erhalten', 'status', 'kommentar', 'engel_handle', 'twitter_handle')


@admin.register(Kiffel)
class KiffelAdmin(ImportExportMixin, admin.ModelAdmin):
    # admin list table view
    list_display = ['nickname', 'vorname', 'nachname', 'email', 'student',
                    'datum_bezahlt', 'datum_tshirt_erhalten']
    list_display_links = ['nickname']

    # import format options
    formats = (base_formats.CSV,)
    resource_class = KiffelResource
