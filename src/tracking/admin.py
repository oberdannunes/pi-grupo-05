from importlib.resources import path

from django.contrib import admin

from django.contrib.auth.models import Group, User
from .views.admin.admin_uploadform import UploadForm
from .views.admin.admin_orderadmin import OrderAdmin

# Removendo os modelos Group e User do admin para simplificar a interface
admin.site.unregister(Group)
admin.site.unregister(User) 

# Personalizando o título e o cabeçalho do site de administração
admin.site.site_title = "FastLog"
admin.site.site_header = "FastLog - Administração"
admin.site.index_title = "Gerenciamento de dados"
 