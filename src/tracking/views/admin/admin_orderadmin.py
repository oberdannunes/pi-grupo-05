from django.contrib import admin
from tracking.models import Order
from admin_extra_buttons.api import ExtraButtonsMixin, button
from django.shortcuts import redirect
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.template.response import TemplateResponse
from .admin_uploadform import UploadForm
from tracking.services.order_excel_import import OrderExcelImportService

@admin.register(Order)
class OrderAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ( "nfe", "customer_cnpj", "customer", "carrier", "order_date", "delivery_date", "status")
       
    @button(label='Upload planilha de carga', icon='fa-solid fa-upload', order=1)
    def upload(self, request):
        context = self.get_common_context(request, title='Upload planilha de carga')
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                downloaded_file = request.FILES['docfile']
                
                import_service = OrderExcelImportService()
                import_service.importfile(downloaded_file)   
                
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
    