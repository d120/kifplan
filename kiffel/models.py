from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)

from kiffel.helper import EAN8

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        u = self.create_user(email=email, password=password)
        u.is_superuser = True
        u.save(using=self._db)
        return u


class Person(PermissionsMixin, AbstractBaseUser):
    """ repräsentiert eine angemeldete Person, was auch immer sie (nicht) ist """

    class Meta:
        ordering = ('nickname',)
        verbose_name = 'Person'
        verbose_name_plural = 'Personen'
        permissions = (
            ('import_persons', 'Import new persons'),
        )

    # Felder aus der Anmeldung (orga.fachschaften.org)
    nickname = models.CharField(null=True, blank=True, max_length=100, verbose_name='Nickname (Namensschild)')
    vorname = models.CharField(null=True, blank=True, max_length=100)
    nachname = models.CharField(null=True, blank=True, max_length=100)
    student = models.BooleanField(default=False)
    hochschule = models.CharField(null=True, blank=True, max_length=100, verbose_name='Hochschule/Ort/Verein')
    kommentar_public = models.TextField(null=True, blank=True, verbose_name='Kommentar öffentlich')
    kommentar_orga = models.TextField(null=True, blank=True, verbose_name='Kommentar Orga')
    anreise_geplant = models.DateTimeField(null=True, blank=True)
    abreise_geplant = models.DateTimeField(null=True, blank=True)
    ernaehrungsgewohnheit = models.CharField(max_length=100, null=True, blank=True,
        verbose_name='Ernährungsgewohnheit')
    lebensmittelunvertraeglichkeiten = models.CharField(max_length=400, null=True, blank=True,
        verbose_name='Lebensmittelunverträglichkeiten')
    volljaehrig = models.BooleanField(default=False, verbose_name='Volljährig (über 18)')
    eigener_schlafplatz = models.BooleanField(default=False, verbose_name='Hat eigenen Schlafplatz')
    tshirt_groesse = models.CharField(null=True, blank=True, max_length=10, verbose_name='T-Shirt-Größe')
    nickname_auf_tshirt = models.BooleanField(default=False, verbose_name='Nickname auf T-Shirt drucken')
    kapuzenjacke_groesse = models.CharField(max_length=10, null=True, blank=True,
        verbose_name='Kapuzenjacke (evtl. Größe)')
    nickname_auf_kapuzenjacke = models.BooleanField(default=False, verbose_name='Nickname auf Kapuzenjacke drucken')
    weitere_tshirts = models.CharField(max_length=100, null=True, blank=True, verbose_name='Weitere T-Shirts')
    interesse_theater = models.BooleanField(default=False, verbose_name='Interesse an Theaterbesuch')
    interesse_esoc = models.BooleanField(default=False, verbose_name='Interesse an ESOC-Führung')
    anmeldung_angelegt = models.DateTimeField(null=True, blank=True)
    anmeldung_aktualisiert = models.DateTimeField(null=True, blank=True)

    # Orga-Status
    kommentar = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    datum_bezahlt = models.DateTimeField(null=True, blank=True, verbose_name='Tn.beitrag bezahlt')
    datum_tuete_erhalten = models.DateTimeField(null=True, blank=True, verbose_name='Tüte erhalten')
    datum_tshirt_erhalten = models.DateTimeField(null=True, blank=True, verbose_name='T-Shirt erhalten')
    datum_teilnahmebestaetigung_erhalten = models.DateTimeField(null=True, blank=True,
        verbose_name='Teilnahmebestätigung erhalten')
    twitter_handle = models.CharField(max_length=100, null=True, blank=True, verbose_name='Twitter-Handle')

    # KDV-System
    kdv_id = models.CharField(max_length=32, null=True, blank=True, verbose_name='KDV-ID', unique=True)

    # Typ dieses Eintrags
    ist_kiffel = models.BooleanField(default=False, verbose_name='Person ist Kiffel')
    ist_orga = models.BooleanField(default=False, verbose_name='Person ist Orga')
    ist_helfer = models.BooleanField(default=False, verbose_name='Person ist Helfer')
    ist_anonym = models.BooleanField(default=False, verbose_name='Person ist Anonym')

    # Matching mit Importsystemen
    engel_id = models.IntegerField(null=True, blank=True)
    anmeldung_id = models.IntegerField(null=True, blank=True)

    # User fields
    email = models.EmailField(null=True, blank=True, verbose_name='E-Mail', unique=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def renew_kdv_barcode(self):
        """
        Generates new unique EAN 8 barcodes for selected kiffels
        """
        self.kdv_id = EAN8.get_random()
        while Person.objects.filter(kdv_id=self.kdv_id).count() > 0:
            self.kdv_id = EAN8.get_random()
        self.save()
    
    def get_full_name(self):
        return "{0} {1}".format(self.vorname, self.nachname)

    def get_short_name(self):
        return self.nickname

    def __str__(self):
        return "{0} ({1})".format(self.nickname, self.email)

    @property
    def is_staff(self):
        return self.is_superuser or self.ist_orga

    @property
    def is_active(self):
        return self.is_superuser or self.ist_orga

