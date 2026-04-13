from django.db import models

class State(models.Model):
    id = models.CharField(max_length=2, unique=True, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name