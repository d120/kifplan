from django.contrib import admin
from django import forms
from django.db import models
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats
from django.contrib.admin.filters import FieldListFilter
from kiffel.models import Person, KDVUserBarcode
from kiffel.resources import KiffelResource
import kiffel.admin_actions
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm
from datetime import datetime
from django.contrib.auth.views import password_reset
from django.conf.urls import url
from django.contrib import auth

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, UserChangeForm, UserCreationForm,
)
from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


class DropdownDatetimeWidget(forms.Select):
    def __init__(self, attrs=None):
        choices = (
            ('', 'Nein'),
            ('Now', 'Ja - jetzt'),
            ('Keep', 'Ja - Wert beibehalten'),
        )
        super(DropdownDatetimeWidget, self).__init__(attrs, choices)
    def render(self, name, value, attrs=None):
        print("render: ",value, self.choices)
        if value == None:
            value = ''
            self.choices.pop()
        elif value != None:
            #value = 'Keep'
            self.choices[2] = (str(value), 'Ja - ' + str(value))
        print("render2: ",value, self.choices)
        return super(DropdownDatetimeWidget, self).render(name, value, attrs)
    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        print("before:",value)
        if value == 'Now': return datetime.now()
        
        print("after:",value)
        return value


class IsNullListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__isnull' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg)
        super(IsNullListFilter, self).__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, changelist):
        for lookup, title in (
                (None, 'Alle'),
                ('False', 'Ja'),
                ('True', 'Nein')):
            yield {
                'selected': self.lookup_val == lookup,
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg: lookup,
                }),
                'display': title,
            }


class KiffelAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        widgets = {
            #'datum_bezahlt': forms.TextInput(), 
            #'datum_tuete_erhalten': DropdownDatetimeWidget(), 
            #'datum_tshirt_erhalten': DropdownDatetimeWidget(), 
            #'datum_teilnahmebestaetigung_erhalten': DropdownDatetimeWidget(),
        }
        exclude = ()
    password = ReadOnlyPasswordHashField(
          label= ("Password"),
          help_text= ("Raw passwords are not stored, so there is no way to see "
                      "this user's password, but you can change the password "
                      "using <a href=\"password/\">this form</a>."))
    def clean(self):
        if (self.cleaned_data.get('ist_kiffel') or self.cleaned_data.get('ist_orga') or
                self.cleaned_data.get('ist_helfer') or self.cleaned_data.get('ist_anonym')):
            pass
        else:
            raise forms.ValidationError("Bitte wähle mindestens eines aus folgenden Feldern aus: ist_kiffel, ist_orga, ist_helfer, ist_anonym -- ansonsten kann kein Namensschild erstellt werden")
        if self.cleaned_data.get('email') == '':
            raise forms.ValidationError("Bitte gib eine E-Mail-Adresse ein")
        return self.cleaned_data

    def save(self, commit=True):
        u = super().save(False)
        if u.password == "" or u.password is None:
            u.set_unusable_password()
        u.save(commit)
        return u

class KDVUserBarcodeInline(admin.StackedInline):
    model = KDVUserBarcode
    fields = ('code',)
    extra = 0
    
@admin.register(Person)
class KiffelAdmin(admin.ModelAdmin):
    form = KiffelAdminForm
    
    def reset_password(self, request, user_id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.model, pk=user_id)

        form = PasswordResetForm(data={'email': user.email})
        form.is_valid()

        form.save(email_template_name='my_template.html')
        return HttpResponseRedirect('..')

    def get_urls(self):
        return [
            url(
                r'^(.+)/password/$',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ] + super(KiffelAdmin, self).get_urls()
    
    # admin list table view
    list_display = ['nickname', 'vorname', 'nachname',
        'datemarks', 'tshirt_groesse', 'hochschule', 'status_desc', 'engel_id_link', ]
    #list_editable = ['hochschule', ]
    list_display_links = ['nickname']
    list_filter = [
        'ist_kiffel', 'ist_orga', 'ist_helfer', 'student', 
        ('datum_bezahlt', IsNullListFilter),
        ('datum_teilnahmebestaetigung_erhalten', IsNullListFilter),
        'hochschule', ]
    search_fields = ['nickname','vorname','nachname','hochschule','email','kdvuserbarcode__code',]
    
    actions = [
            kiffel.admin_actions.generate_nametags,
            kiffel.admin_actions.generate_part_cert,
            kiffel.admin_actions.mark_bezahlt_now,
            kiffel.admin_actions.mark_tuete_erhalten_now,
            kiffel.admin_actions.mark_baendchen_erhalten_now,
            kiffel.admin_actions.mark_teilnahmebestaetigung_erhalten_now,
            kiffel.admin_actions.renew_kdv_barcode,
            kiffel.admin_actions.set_tu_darmstadt,
    ]
    
    
    fieldsets = (
      ('', {
          'fields': ('nickname', 'vorname', 'nachname', 'student', 'hochschule', 
            )
      }),
      ('Teilnahmestatus', {
          'classes': ('collapse',),
          'fields': (
           'kommentar', 'status', 'datum_bezahlt', 'datum_tuete_erhalten', 'datum_baendchen_erhalten', 
           'datum_teilnahmebestaetigung_erhalten', )
      }),
      ('Kleidungsstücke', {
          'classes': ('collapse',),
          'fields': ('tshirt_groesse', 'nickname_auf_tshirt', 'kapuzenjacke_groesse', 'nickname_auf_kapuzenjacke',
           'weitere_tshirts',)
      }),
      ('Details aus der Anmeldung', {
          'classes': ('collapse',),
          'fields': ('anreise_geplant', 'abreise_geplant', 'ernaehrungsgewohnheit', 'lebensmittelunvertraeglichkeiten', 'volljaehrig', 
           'eigener_schlafplatz', 'interesse_theater', 'interesse_esoc', 'kommentar_public', 'kommentar_orga',
             'anmeldung_angelegt', 'anmeldung_aktualisiert', )
      }),
      ('Login-Account', {
          'classes': ('collapse',),
          'fields': ('email', 'password', 
            'ist_kiffel', 'ist_orga', 'ist_helfer', 'ist_anonym', 'is_superuser', 
            'groups', 'user_permissions', 'last_login',)
      }),
      ('crossRef', {
          'classes': ('collapse',),
          'fields': ('engel_id', 'anmeldung_id', 'twitter_handle', 'kdv_balance', )
      }),
    )
    
    inlines = [
        KDVUserBarcodeInline,
    ]
    
    
    change_password_form = AdminPasswordChangeForm
    change_user_password_template = None
    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = self.get_object(request, unquote(id))
        if user is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': force_text(self.model._meta.verbose_name),
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        context.update(self.admin_site.each_context(request))

        request.current_app = self.admin_site.name

        return TemplateResponse(request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context)
    
