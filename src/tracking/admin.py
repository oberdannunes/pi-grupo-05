from importlib.resources import path

from django import forms
from django.contrib import admin
from .models import Country, State, City, Order
from admin_extra_buttons.api import ExtraButtonsMixin, button
from django.shortcuts import redirect
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.template.response import TemplateResponse


admin.site.register(Country)
   
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("name", "country")

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "country")
    
    def country(self, obj):
        return obj.state.country

    country.short_description = "Country"

class UploadForm(forms.Form):
    docfile = forms.FileField(label='Planilha para carga')

@admin.register(Order)
class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    @button(label='Upload planilha de carga', icon='fa-solid fa-upload', order=1)
    def upload(self, request):
        context = self.get_common_context(request, title='Upload')
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