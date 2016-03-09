from django.db import models

class Kiffel(models.Model):
    """ repräsentiert einen angemeldeten Kiffel """

    # Felder aus der Anmeldung (orga.fachschaften.org)
    nickname = models.CharField(max_length=100)
    vorname = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100)
    email = models.EmailField()
    student = models.BooleanField()
    hochschule = models.CharField(max_length=100) # Hochschule/Ort/Verein
    kommentar_public = models.TextField(null=True, blank=True)
    kommentar_orga = models.TextField(null=True, blank=True)
    anreise_geplant = models.DateTimeField()
    abreise_geplant = models.DateTimeField()
    ernaehrungsgewohnheit = models.CharField(max_length=100, null=True, blank=True)
    lebensmittelunvertraeglichkeiten = models.CharField(max_length=400, null=True, blank=True)
    volljaehrig = models.BooleanField()
    eigener_schlafplatz = models.BooleanField()
    tshirt_groesse = models.CharField(max_length=10)
    nickname_auf_tshirt = models.BooleanField()
    kapuzenjacke_groesse = models.CharField(max_length=10, null=True, blank=True)
    nickname_auf_kapuzenjacke = models.BooleanField()
    weitere_tshirts = models.CharField(max_length=100, null=True, blank=True)
    interesse_theater = models.BooleanField()
    interesse_esoc = models.BooleanField()
    anmeldung_angelegt = models.DateTimeField()
    anmeldung_aktualisiert = models.DateTimeField()

    # zusätzliche Felder gemäß Spezifikation
    datum_bezahlt = models.DateTimeField(null=True, blank=True)
    datum_tshirt_erhalten = models.DateTimeField(null=True, blank=True)
    datum_teilnahmebestaetigung_erhalten = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    kommentar = models.TextField(null=True, blank=True)
    engel_handle = models.CharField(max_length=100, null=True, blank=True)
    twitter_handle = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('nickname',)
