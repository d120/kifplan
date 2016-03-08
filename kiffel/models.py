from django.db import models

class Kiffel(models.Model):
    # Felder aus der Anmeldung (orga.fachschaften.org)
    nickname = models.CharField(max_length=100)
    vorname = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100)
    email = models.EmailField()
    student = models.BooleanField()
    hochschule = models.CharField(max_length=100) # Hochschule/Ort/Verein
    kommentar_public = models.TextField()
    kommentar_orga = models.TextField()
    anreise_geplant = models.DateTimeField()
    abreise_geplant = models.DateTimeField()
    ernaehrungsgewohnheit = models.CharField(max_length=100)
    lebensmittelunvertraeglichkeiten = models.CharField(max_length=400)
    volljaehrig = models.BooleanField()
    eigener_schlafplatz = models.BooleanField()
    tshirt_groesse = models.CharField(max_length=10)
    nickname_auf_tshirt = models.BooleanField()
    kapuzenjacke = models.BooleanField()
    nickname_auf_kapuzenjacke = models.BooleanField()
    weitere_tshirts = models.IntegerField()
    interesse_theater = models.BooleanField()
    interesse_esoc = models.BooleanField()
    anmeldung_angelegt = models.DateTimeField()
    anmeldung_aktualisiert = models.DateTimeField()

    # zusätzliche Felder gemäß Spezifikation
    datum_bezahlt = models.DateTimeField(null=True)
    datum_tshirt_erhalten = models.DateTimeField(null=True)
    datum_teilnahmebestaetigung_erhalten = models.DateTimeField(null=True)
    status = models.CharField(max_length=100)
    kommentar = models.TextField()
    engel_handle = models.CharField(max_length=100)
    twitter_handle = models.CharField(max_length=100)

    class Meta:
        ordering = ('nickname',)
