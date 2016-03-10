from random import randint
import tempfile, os, shutil
from subprocess import Popen, PIPE
from django.template.loader import get_template
from import_export.widgets import Widget


class EAN8:
    def get_random():
        code = str(randint(1000000, 9999999))
        weighed_sum = int(code[0])*3 + int(code[1])*1 + int(code[2])*3 + \
            int(code[3])*1 + int(code[4])*3 + int(code[5])*1 + int(code[6])*3
        checksum = (10 - (weighed_sum % 10)) % 10
        code = code + str(checksum)
        return code


class QueryFilter:
    def filter(queryset, request, fields):
        for field in fields:
            value = request.GET.get(field, None)
            if value is not None:
                queryset = queryset.filter(**{ field+'__iexact': value })
        return queryset


class JaNeinBooleanWidget(Widget):
    def clean(value):
        return True if value == "Ja" else False
    def render(value):
        return "Ja" if value else "Nein"


class LaTeX:
    def escape(queryset):
        for item in queryset:
            for key, value in item.__dict__.items():
                if isinstance(value, str):
                    item.__dict__[key] = value.replace('_', '\_')
        return queryset

    def render(queryset, template_name, assets):
        items = LaTeX.escape(queryset)
        template = get_template(template_name)
        rendered_tpl = template.render({'kiffels': items}).encode('utf-8')
        with tempfile.TemporaryDirectory() as tempdir:
            for asset in assets:
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/assets/'+asset, tempdir)
            for i in range(2):
                process = Popen(
                    ['pdflatex'],
                    stdin=PIPE,
                    stdout=PIPE,
                    cwd=tempdir,
                )
                process.communicate(rendered_tpl)
            with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                pdf = f.read()
        return pdf
