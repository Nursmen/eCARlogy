from django.db import models

# Create your models here.
# my model should consist of charfield and URLField

class Eminem(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name