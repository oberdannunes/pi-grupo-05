from django.db import models

class Order(models.Model):
    order_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return str(self.order_date)