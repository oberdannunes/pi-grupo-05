from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    def __str__(self):
        return self.name