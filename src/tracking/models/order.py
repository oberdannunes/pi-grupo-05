from django.db import models

class Order(models.Model):
    order_date = models.DateField()
    
    def __str__(self):
        return str(self.order_date)