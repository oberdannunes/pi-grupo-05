from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Cidade") 
    state = models.ForeignKey('State', on_delete=models.CASCADE, verbose_name="Estado")

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        # ✅ ADICIONE esta restrição: A combinação de Nome e Estado deve ser única
        constraints = [
            models.UniqueConstraint(fields=['name', 'state'], name='unique_city_state')
        ]

    def __str__(self):
        return f"{self.name} - {self.state_id}"