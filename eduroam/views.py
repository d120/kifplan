
from django.views.generic import View
from django.db import IntegrityError
from eduroam.models import GuestAccount
import re, datetime
from django.shortcuts import render


class ImportGuestAccounts(View):
    def get(self, request, *args, **kwargs):
        foo = ""
        return render(request, "kiffel/import_csv_template.html", { 'title': 'Eduroam Gastaccounts importieren', 'output': '' })
    
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('eduroam.create_guestaccount'):
            raise PermissionDenied
        lines = request.POST["content"].splitlines(False)
        
        out = "Importiere Gastaccounts\n   "
        accname = ""
        accpass = ""
        von = ""
        bis = ""
        for line in lines:
            d = line.split(':')
            match = re.match(".*von ([0-9.]+) bis ([0-9.]+).*", line)
            if match:
                von = match.group(1)
                bis = match.group(2)
            elif len(d) == 2:
                if 'Accountname' in d[0]:
                    accname = d[1].strip()
                    out += " name: "+accname
                if 'Passwort' in d[0]:
                    accpass = d[1].strip()
                    out += " pass: "+accpass
                    try:
                        GuestAccount.objects.create(login=accname, password=accpass, vergeben=False,
                                    gueltig_von=datetime.datetime.strptime(von, '%d.%m.%Y'),
                                    gueltig_bis=datetime.datetime.strptime(bis, '%d.%m.%Y'))
                        out += " ok\n   "
                    except IntegrityError as ex:
                        out += " fail: "+str(ex)+"\n   "
                
        out += "OK"
        
        return render(request, "kiffel/import_csv_template.html", { 'title': 'Eduroam Gastaccounts importieren', 'output': out })
