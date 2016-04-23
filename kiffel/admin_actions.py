from kiffel.models import Person
from kiffel.helper import EAN8, LaTeX
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

def renew_kdv_barcode(modeladmin, request, queryset):
    """
    Generates new unique EAN 8 barcodes for selected people
    """
    for kiffel in queryset:
        kiffel.kdv_id = EAN8.get_random()
        while Person.objects.filter(kdv_id=kiffel.kdv_id).count() > 0:
            kiffel.kdv_id = EAN8.get_random()
        kiffel.save()

renew_kdv_barcode.short_description = 'Neue KDV-Barcodes generieren'


def generate_part_cert(modeladmin, request, queryset):
    """
    Generates a PDF file with participation certificates for selected people and sends it to the browser
    """
    items = LaTeX.escape(queryset)
    (pdf, pdflatex_output) = LaTeX.render(items, 'kiffel/attending-report.tex', ['bilder/KIFLogo-Schrift.jpg', 'scheine.sty'])
    if pdf == None:
        return render(request, "kiffel/import_csv_template.html", { "titel": "ERROR:","content": pdflatex_output[0].decode("utf-8") })
    r = HttpResponse(content_type='application/pdf')
    r['Content-Disposition'] = 'attachment; filename=kiffels-attending-reports.pdf'
    r.write(pdf)
    return r

generate_part_cert.short_description = 'Teilnahmebestätigungen drucken'


def generate_nametags(modeladmin, request, queryset):
    """
    Generates a PDF file with name tags for selected people and sends it to the browser
    """
    items = LaTeX.escape(queryset)
    (pdf, pdflatex_output) = LaTeX.render(items, 'kiffel/nametags.tex', ['bilder/kif_logo.png', 'namensschilder.sty'])
    if pdf == None:
        return render(request, "kiffel/import_csv_template.html", { "titel": "ERROR:","content": pdflatex_output[0].decode("utf-8") })
    r = HttpResponse(content_type='application/pdf')
    r['Content-Disposition'] = 'attachment; filename=kiffels-nametags.pdf'
    r.write(pdf)
    return r

generate_nametags.short_description = 'Namensschilder drucken'


def mark_bezahlt_now(modeladmin, request, queryset):
    """
    Sets datum_bezahlt to now for all selected people.
    """
    queryset.update(datum_bezahlt = datetime.now())
mark_bezahlt_now.short_description = 'Als "Teilnahmebeitrag bezahlt" markieren'


def mark_tuete_erhalten_now(modeladmin, request, queryset):
    """
    Sets datum_bezahlt to now for all selected people.
    """
    queryset.update(datum_tuete_erhalten = datetime.now())
mark_tuete_erhalten_now.short_description = 'Als "Tüte erhalten" markieren'

def mark_tshirt_erhalten_now(modeladmin, request, queryset):
    """
    Sets datum_bezahlt to now for all selected people.
    """
    queryset.update(datum_tshirt_erhalten = datetime.now())
mark_tshirt_erhalten_now.short_description = 'Als "T-Shirt erhalten" markieren'


def mark_teilnahmebestaetigung_erhalten_now(modeladmin, request, queryset):
    """
    Sets datum_bezahlt to now for all selected people.
    """
    queryset.update(datum_teilnahmebestaetigung_erhalten = datetime.now())
mark_teilnahmebestaetigung_erhalten_now.short_description = 'Als "Teilnahmebestätigung erhalten" markieren'

