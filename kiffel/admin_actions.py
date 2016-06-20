from kiffel.models import Person
from kiffel.helper import EAN8, LaTeX
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import csv , io

def renew_kdv_barcode(modeladmin, request, queryset):
    filename = '/tmp/oskiosk.csv'
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)

        for kiffel in queryset:
            # Generates unique EAN 8 barcode if the barcode field is empty
            if kiffel.kdvuserbarcode_set.count() == 0:
                kiffel.kdvuserbarcode_set.create(code=EAN8.get_random())

            hochschule = "n/a"
            if kiffel.hochschule: hochschule=kiffel.hochschule
            csvwriter.writerow([ kiffel.nickname, kiffel.kdvuserbarcode_set.first().code, hochschule ])

    with open(filename) as x: csvstring = x.read()

    return render(request, "kiffel/import_csv_template.html", { "titel": "CSV-Datei zum Import in die KDV:","content": csvstring,
        "output": """<b>Die CSV-Datei wurde auf dem Server unter /tmp/oskiosk.csv abgelegt und kann wie folgt importiert werden:</b>
        su kdv
        RAILS_ENV=production rake 'import:boon:users[/tmp/oskiosk.csv]'
        """})

renew_kdv_barcode.short_description = 'KDV-Steuerdatei generieren'


def set_tu_darmstadt(modeladmin, request, queryset):
    for kiffel in queryset:
        kiffel.hochschule="TU Darmstadt"
        kiffel.save()
set_tu_darmstadt.short_description = 'Auf TU Darmstadt zuweisen'


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
    if pdf == None or len(pdf) == 0:
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

def mark_baendchen_erhalten_now(modeladmin, request, queryset):
    """
    Sets datum_bezahlt to now for all selected people.
    """
    queryset.update(datum_baendchen_erhalten = datetime.now())
mark_baendchen_erhalten_now.short_description = 'Als "Bändchen erhalten" markieren'


def mark_teilnahmebestaetigung_erhalten_now(modeladmin, request, queryset):
    """
    Sets datum_bezahlt to now for all selected people.
    """
    queryset.update(datum_teilnahmebestaetigung_erhalten = datetime.now())
mark_teilnahmebestaetigung_erhalten_now.short_description = 'Als "Teilnahmebestätigung erhalten" markieren'
