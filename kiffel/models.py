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

        if password is None:
            user.set_unusable_password()
        else:
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
            ('resetpw_person', 'Reset a persons password'),
        )

    # Felder aus der Anmeldung (orga.fachschaften.org)
    nickname = models.CharField(null=True, blank=True, max_length=100, verbose_name='Nickname')
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
    datum_baendchen_erhalten = models.DateTimeField(null=True, blank=True, verbose_name='Bändchen erhalten')
    datum_teilnahmebestaetigung_erhalten = models.DateTimeField(null=True, blank=True,
        verbose_name='Teilnahmebestätigung erhalten')
    twitter_handle = models.CharField(max_length=100, null=True, blank=True, verbose_name='Twitter-Handle')

    # KDV-System
    kdv_balance = models.IntegerField(default=0)
    
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
    is_active = models.BooleanField(default=True, verbose_name='Benutzer kann sich einloggen')
    
    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def status_desc(self):
        o = ""
        if self.ist_orga: o += "<b><font color=green>Orga</font></b> "
        if self.ist_helfer: o += "<b><font color=#884411>Helfer</font></b> "
        if self.ist_kiffel: o += "Kiffel "
        if self.ist_anonym: o += "Anonym "
        return o
    status_desc.allow_tags = True
    status_desc.short_description = 'Person ist'
    status_desc.admin_order_field = 'ist_helfer'
    
    def engel_id_link(self):
        if self.engel_id == None: return '--'
        return '<a href="%s%s">➜ %s</a>' % ('https://www2.fachschaft.informatik.tu-darmstadt.de/engelsystem/?p=users&action=view&user_id=', self.engel_id, self.engel_id)
    engel_id_link.allow_tags = True
    engel_id_link.short_description = 'Engel-ID'
    engel_id_link.admin_order_field = 'engel_id'
    
    def get_full_name(self):
        return "{0} {1}".format(self.vorname, self.nachname)

    def get_short_name(self):
        return self.nickname
    
    def get_barcode(self):
        return self.kdvuserbarcode_set.first().code[-8:]
    
    def __str__(self):
        return "{0} ({1})".format(self.nickname, self.email)

    def get_datemark(self, icon, field_name):
        # der Event Handler hierzu ist in static/kiffel/kiffelhelper.js definiert
        val = getattr(self, field_name)
        title = Person._meta.get_field(field_name).verbose_name
        if val != None:
            state = "datemark-yes"
            title += ": ja, am " + str(val)
        else:
            state = "datemark-no"
            title += ": nein"
        return "<span class='datemark "+state+"' title='"+title+"' data-mark-id='"+str(self.id)+"' data-mark-field='"+field_name+"'><i class='fa fa-"+icon+"'></i></span>"
    
    def datemarks(self):
        o = ""
        o += self.get_datemark('money', 'datum_bezahlt')
        o += self.get_datemark('shopping-bag', 'datum_tuete_erhalten')
        o += self.get_datemark('glide-g', 'datum_baendchen_erhalten')
        o += self.get_datemark('file-text', 'datum_teilnahmebestaetigung_erhalten')
        return "<nobr>" + o + "</nobr>"
    datemarks.short_description = "stuff"
    datemarks.allow_tags = True

    def mobile_datemarks(self):
        o = ""
        o += self.get_datemark('glide-g', 'datum_baendchen_erhalten')
        return "<nobr>" + o + "</nobr>"
    datemarks.short_description = "mobile stuff"
    datemarks.allow_tags = True
    

    @property
    def is_staff(self):
        return self.is_superuser or self.ist_orga or self.ist_helfer



class KDVUserBarcode(models.Model):
    class Meta:
        db_table  = 'kdv_user_identifiers'
        managed = False
    
    code = models.CharField(null=True, blank=True, max_length=255, verbose_name='Barcode')
    identifiable = models.ForeignKey(Person, on_delete=models.CASCADE)
    identifiable_type = models.CharField(max_length=255, default='User') #models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #identifiable = GenericForeignKey('identifiable_type', 'identifiable_id')
    
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    def __str__(self):
        return self.code

