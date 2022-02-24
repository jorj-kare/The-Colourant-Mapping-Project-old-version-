from django.db import models
from django.db.models.fields import CharField, EmailField, TextField, IntegerField
from django.urls import reverse


class Colourants(models.Model):

    colour = CharField(max_length=200)
    pigment = CharField(max_length=200)
    techniques = CharField(max_length=500,blank=True,)
    chronology_from = IntegerField()
    chronology_to = IntegerField()
    archeological_context = TextField(max_length=1000,blank=True)
    context = CharField(max_length=200)
    references = CharField(max_length=500,blank=True)
    notes = TextField(max_length=1000, blank=True)
    location = TextField(max_length=500, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    affiliation = models.CharField(max_length=200, blank=True)
    publicly_available = models.BooleanField()
    created_date = models.DateTimeField(auto_now=True)
    check = models.BooleanField(default=False)

    def __str__(self):
        return self.colour

    def get_absolute_url(self):
        return reverse("colourants-detail", args=[str(self.id)])
