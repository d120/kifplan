from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class KDVProduct(models.Model):
    class Meta:
        db_table  = 'products'
        verbose_name = 'KDV-Produkt'
        verbose_name_plural = 'KDV-Produkte'
    name = models.CharField(null=True, blank=True, max_length=255, verbose_name='Produktname')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    def __str__(self):
        return self.name

class KDVProductBarcode(models.Model):
    class Meta:
        db_table  = 'kdv_product_identifiers'
    code = models.CharField(null=True, blank=True, max_length=255, verbose_name='Barcode')
    identifiable = models.ForeignKey(KDVProduct, on_delete=models.CASCADE)
    identifiable_type = models.CharField(max_length=255, default='Product') #models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #identifiable = GenericForeignKey('identifiable_type', 'identifiable_id')
    
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    def __str__(self):
        return self.code

class KDVUser(models.Model):
    class Meta:
        db_table  = 'users'
        verbose_name = 'KDV-User'
    name = models.CharField(null=True, blank=True, max_length=255, verbose_name='Name')
    balance = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    allow_negative_balance = models.BooleanField()
    def __str__(self):
        return self.name
    
class KDVUserBarcode(models.Model):
    class Meta:
        db_table  = 'kdv_user_identifiers'
    code = models.CharField(null=True, blank=True, max_length=255, verbose_name='Barcode')
    identifiable = models.ForeignKey(KDVUser, on_delete=models.CASCADE)
    identifiable_type = models.CharField(max_length=255, default='User') #models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #identifiable = GenericForeignKey('identifiable_type', 'identifiable_id')
    
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    def __str__(self):
        return self.code

class KDVPricing(models.Model):
    class Meta:
        db_table  = 'pricings'
    
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(KDVProduct, on_delete=models.CASCADE)
    #identifiable = GenericForeignKey('identifiable_type', 'identifiable_id')
    
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    def __str__(self):
        return "%0.02f" % (self.price/100)

