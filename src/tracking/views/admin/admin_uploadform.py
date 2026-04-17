import os
from django import forms

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
                
        return file