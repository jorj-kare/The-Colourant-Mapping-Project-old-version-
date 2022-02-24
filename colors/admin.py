from django.contrib import admin
from .models import Colourants

# Register your models here.


@admin.register(Colourants)
class ColourantAdmin(admin.ModelAdmin):
    list_display = ('colour','pigment', 'chronology_from',
                    'chronology_to', 'location',)
