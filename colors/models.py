from django.db import models
from django.db.models.fields import CharField, EmailField, TextField, IntegerField
from django.urls import reverse


class Colourants(models.Model):

    colour = CharField(max_length=200)
    pigment = CharField(max_length=200)
    techniques = TextField(blank=True, max_length=4000)
    chronology_from = IntegerField(blank=True,null=True)
    chronology_to = IntegerField(blank=True,null=True)
    archeological_context = TextField(blank=True, max_length=4000)
    category_of_find = TextField(max_length=4000)
    references = TextField(blank=True,max_length=4000)
    notes = TextField( blank=True,max_length=4000)
    location = TextField( blank=True,max_length=4000)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True,null=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True,null=True)
    name = models.CharField( blank=True,max_length=200)
    email = models.EmailField( blank=True,max_length=200)
    affiliation = models.TextField( blank=True,max_length=4000)
    publicly_available = models.BooleanField()
    created_date = models.DateTimeField(auto_now=True)
    check = models.BooleanField(default=False)

    def __str__(self):
        return self.colour

    def get_absolute_url(self):
        return reverse("colourants-detail", args=[str(self.id)])
