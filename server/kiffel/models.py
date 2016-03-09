from django.db import models

class Kiffel(models.Model):
    """ repräsentiert einen angemeldeten Kiffel """

    # Felder aus der Anmeldung (orga.fachschaften.org)
    nickname = models.CharField(max_length=100, verbose_name='Nickname (Namensschild)')
    vorname = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='E-Mail')
    student = models.BooleanField()
    hochschule = models.CharField(max_length=100, verbose_name='Hochschule/Ort/Verein')
    kommentar_public = models.TextField(null=True, blank=True, verbose_name='Kommentar öffentlich')
    kommentar_orga = models.TextField(null=True, blank=True, verbose_name='Kommentar Orga')
    anreise_geplant = models.DateTimeField()
    abreise_geplant = models.DateTimeField()
    ernaehrungsgewohnheit = models.CharField(max_length=100, null=True, blank=True,
        verbose_name='Ernährungsgewohnheit')
    lebensmittelunvertraeglichkeiten = models.CharField(max_length=400, null=True, blank=True,
        verbose_name='Lebensmittelunverträglichkeiten')
    volljaehrig = models.BooleanField(verbose_name='Volljährig (über 18)')
    eigener_schlafplatz = models.BooleanField(verbose_name='Hat eigenen Schlafplatz')
    tshirt_groesse = models.CharField(max_length=10, verbose_name='T-Shirt-Größe')
    nickname_auf_tshirt = models.BooleanField(verbose_name='Nickname auf T-Shirt drucken')
    kapuzenjacke_groesse = models.CharField(max_length=10, null=True, blank=True,
        verbose_name='Kapuzenjacke (evtl. Größe)')
    nickname_auf_kapuzenjacke = models.BooleanField(verbose_name='Nickname auf Kapuzenjacke drucken')
    weitere_tshirts = models.CharField(max_length=100, null=True, blank=True, verbose_name='Weitere T-Shirts')
    interesse_theater = models.BooleanField(verbose_name='Interesse an Theaterbesuch')
    interesse_esoc = models.BooleanField(verbose_name='Interesse an ESOC-Führung')
    anmeldung_angelegt = models.DateTimeField()
    anmeldung_aktualisiert = models.DateTimeField()

    # zusätzliche Felder gemäß Spezifikation
    datum_bezahlt = models.DateTimeField(null=True, blank=True, verbose_name='Teilnahmebeitrag bezahlt (Datum)')
    datum_tshirt_erhalten = models.DateTimeField(null=True, blank=True, verbose_name='T-Shirt erhalten (Datum)')
    datum_teilnahmebestaetigung_erhalten = models.DateTimeField(null=True, blank=True,
        verbose_name='Teilnahmebestätigung erhalten (Datum)')
    status = models.CharField(max_length=100, null=True, blank=True)
    kommentar = models.TextField(null=True, blank=True)
    engel_handle = models.CharField(max_length=100, null=True, blank=True, verbose_name='Name im Engelsystem')
    twitter_handle = models.CharField(max_length=100, null=True, blank=True, verbose_name='Twitter-Handle')

    class Meta:
        ordering = ('nickname',)
