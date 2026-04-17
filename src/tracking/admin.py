from importlib.resources import path
import os

from django import forms
from django.contrib import admin
from .models import Country, State, City, Order
from admin_extra_buttons.api import ExtraButtonsMixin, button
from django.shortcuts import redirect
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.template.response import TemplateResponse

from django.contrib.auth.models import Group, User

# Removendo os modelos Group e User do admin para simplificar a interface
admin.site.unregister(Group)
admin.site.unregister(User) 

# Personalizando o título e o cabeçalho do site de administração
admin.site.site_title = "FastLog"
admin.site.site_header = "FastLog - Administração"
admin.site.index_title = "Gerenciamento de dados"

class UploadForm(forms.Form):
    docfile = forms.FileField(
        label='Planilha para carga',
        widget=forms.FileInput(attrs={'accept': '.xlsx'})
    )
    
    def clean_docfile(self):
        file = self.cleaned_data.get('docfile')

        if file:
            ext = os.path.splitext(file.name)[1].lower()

            if ext != '.xlsx':
                raise forms.ValidationError(
                    'Arquivo inválido. Envie apenas arquivos .xlsx.'
                )
                
        # Se o arquivo for válido, ele será processado       
        
        #le linhas
        
        # valida
        # se ok, insere
        # se não ok, insere na planilha de erros    


        return file

@admin.register(Order)
class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ( "nfe", "customer", "carrier", "order_date", "delivery_date", "status")
       
    @button(label='Upload planilha de carga', icon='fa-solid fa-upload', order=1)
    def upload(self, request):
        context = self.get_common_context(request, title='Upload planilha de carga')
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                downloaded_file = request.FILES['docfile']
                # process file
                ...
                ...
                return redirect(admin_urlname(context['opts'], 'changelist'))
        else:
            form = UploadForm()
        
        context['form'] = form
        return TemplateResponse(request, 'admin_extra_buttons/orders_upload.html', context)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj = ...):
        return False

    def has_change_permission(self, request, obj = ...):
        return False
    
 