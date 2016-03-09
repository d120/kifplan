from kiffel.models import Kiffel
from kiffel.helper import EAN8

def renew_kdv_barcode(modeladmin, request, queryset):
    """
    Generates new unique EAN 8 barcodes for selected kiffels
    """
    for kiffel in queryset:
        kiffel.kdv_id = EAN8.get_random()
        while Kiffel.objects.filter(kdv_id=kiffel.kdv_id).count() > 0:
            kiffel.kdv_id = EAN8.get_random()
        kiffel.save()

renew_kdv_barcode.short_description = 'Neue KDV-Barcodes generieren'
