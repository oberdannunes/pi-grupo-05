from django.db import models

class Carrier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cnpj = models.CharField(max_length=14, verbose_name='CNPJ', default='')
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name