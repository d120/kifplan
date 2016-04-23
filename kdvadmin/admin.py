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
    list_display = ('name', 'get_barcodes',)
    def get_barcodes(self, obj):
        return ", ".join([x.code for x in obj.barcodes])
        
    inlines = [
        KDVProductPricingInline,
        KDVProductBarcodeInline,
    ]
    
class KDVUserBarcodeInline(admin.StackedInline):
    model = KDVUserBarcode
    fields = ('code',)
    extra = 0
    
@admin.register(KDVUser)
class KDVUserAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        KDVUserBarcodeInline,
    ]
    
