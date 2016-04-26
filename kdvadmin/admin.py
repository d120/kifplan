from django.contrib import admin

from kdvadmin.models import *


class KDVProductBarcodeInline(admin.TabularInline):
    model = KDVProductBarcode
    fields = ('code',)
    extra = 0
    min_num = 1

class KDVProductPricingInline(admin.TabularInline):
    model = KDVPricing
    extra = 0
    min_num = 1

@admin.register(KDVProduct)
class KDVProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_lowest_price', 'get_quantity', 'get_barcodes', )
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

