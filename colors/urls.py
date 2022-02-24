from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView


app_name = 'colors'
urlpatterns = [
    path('', views.help_view, name='info'),
    path('new_entry/', views.index, name='index'),
    path('map/', views.pigments_map, name='map'),
    path('contact/', views.contact_view, name='contact'),
    path('colourants/<int:pk>', views.ColourantsDetailView.as_view(),
         name='colourants-detail'),
]
