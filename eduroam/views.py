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


class AssignGuestAccount(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user.nickname
        return render(request, "eduroam/assign_account.html", { 'title': 'eduroam Gastaccount neu vergeben', 'current_user': current_user })

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('eduroam.assign_guestaccount'):
            raise PermissionDenied
        accounts = GuestAccount.objects.filter(vergeben=False)
        if len(accounts) == 0:
            return render(request, "eduroam/assign_account_result.html", { 'title': 'Vergebener eduroam Gastaccount', 'status': 'unavailable' })
        account = accounts[0]
        account.vorname = request.POST.get('vorname', '')
        account.nachname = request.POST.get('nachname', '')
        account.perso_id = request.POST.get('perso_id', '')
        account.vergeben_durch = request.POST.get('vergeben_durch', '')
        account.vergeben = True
        account.vergeben_am = datetime.datetime.now()
        account.save()
        return render(request, "eduroam/assign_account_result.html", { 'title': 'Vergebener eduroam Gastaccount', 'status': 'ok', 'account': account })

