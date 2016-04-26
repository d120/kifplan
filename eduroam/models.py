from django.db import models

class GuestAccount(models.Model):
    """
    repräsentiert einen eduroam Gastaccount, der vom Infopunkt verliehen
    werden kann
    """

    # Account Stammdaten
    login = models.CharField(max_length=100, verbose_name='Accountname', unique=True)
    password = models.CharField(max_length=100, verbose_name='Passwort')
    gueltig_von = models.DateTimeField()
    gueltig_bis = models.DateTimeField()

    # Account Ausleihe
    vergeben = models.BooleanField()
    vorname = models.CharField(max_length=100, null=True, blank=True)
    nachname = models.CharField(max_length=100, null=True, blank=True)
    perso_id = models.CharField(max_length=100, verbose_name='Personalausweisnummer', null=True, blank=True)

    # ausleihender Infopunkt-Engel
    vergeben_am = models.DateTimeField(null=True, blank=True)
    vergeben_durch = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.login
    
    class Meta:
        ordering = ('login',)
        verbose_name = 'Gastaccount'
