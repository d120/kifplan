from django.contrib import admin

from kdvadmin.models import *


class KDVProductBarcodeInline(admin.StackedInline):
    model = KDVProductBarcode
    fields = ('code',)
    extra = 0

class KDVProductPricingInline(admin.StackedInline):
    model = KDVPricing
    extra = 0

@admin.register(KDVProduct)
class KDVProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_barcodes', 'get_lowest_price', 'get_quantity', )
    ordering = ('name',)
    
    inlines = [
        KDVProductPricingInline,
        KDVProductBarcodeInline,
    ]
    
    def get_barcodes(self, obj):
        return ", ".join([x.code for x in obj.kdvproductbarcode_set.all()])
    get_barcodes.short_description = 'Barcode'
    def get_lowest_price(self, obj):
        return "%0.02f" % (min([x.price for x in obj.kdvpricing_set.all()])/100)
    get_lowest_price.short_description = 'Preis'
    def get_quantity(self, obj):
        return sum([x.quantity for x in obj.kdvpricing_set.all()])
    get_quantity.short_description = 'Anzahl'

class KDVUserBarcodeInline(admin.StackedInline):
    model = KDVUserBarcode
    fields = ('code',)
    extra = 0
    
@admin.register(KDVUser)
class KDVUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_barcodes', 'balance', 'allow_negative_balance',)
    ordering = ('name',)
    
    inlines = [
        KDVUserBarcodeInline,
    ]
    
    def get_barcodes(self, obj):
        return ", ".join([x.code for x in obj.kdvuserbarcode_set.all()])
    
    
