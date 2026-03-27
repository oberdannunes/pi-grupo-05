from importlib.resources import path

from django import forms
from django.contrib import admin
from .models import Country, State, City

admin.site.register(Country)
   
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    
    
class CityImportForm(forms.Form):
    file = forms.FileField(label="Arquivo CSV")
    

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "country")
    
    def country(self, obj):
        return obj.state.country

    country.short_description = "Country"