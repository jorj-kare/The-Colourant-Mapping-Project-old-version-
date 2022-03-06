
from django.views.generic import UpdateView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import ColourantsForm, SearchForm, ContextSelectForm, ColourantSelectForm, ChronologySelectForm, ContextOther,ColourOther, PigmentOther,ChronologyOther
from geopy.geocoders import Nominatim
import folium
from colors.models import Colourants
from django.views import generic
from folium.plugins import MarkerCluster
from django.contrib import messages
from django.http import HttpResponseRedirect
from colors.utils import select, chr_format, format_number


def index(request):

    m = folium.Map(min_zoom=2)

    folium.LatLngPopup().add_to(m)
    geolocator = Nominatim(user_agent='colors')

    if request.method == 'POST' and 'search' in request.POST:
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            find = search_form.cleaned_data['find']
            location = geolocator.geocode(find, language='en')
            if location:
                lat = location.latitude
                lon = location.longitude
                m = folium.Map(location=[lat, lon], zoom_start=6.2)
                folium.Marker([lat, lon], popup=location.address).add_to(m)
                folium.LatLngPopup().add_to(m)

            else:
                messages.error(request, "Wrong address!")

    if request.method == 'POST' and 'entries' in request.POST:
        colourants_form = ColourantsForm(request.POST)
        context_other = ContextOther(request.POST)
        colour_other = ColourOther(request.POST)
        chronology_other = ChronologyOther(request.POST)
        pigment_other = PigmentOther(request.POST)
        
        
        if colourants_form.is_valid():

            instance = colourants_form.save(commit=False)

            col_other = request.POST.get('colour_other')
            con_other = request.POST.get('context_other')
            pig_other = request.POST.get('pigment_other')
            chr_other =request.POST.get('chronology_other')
            loc = colourants_form.cleaned_data.get('location')
            Lat = colourants_form.cleaned_data.get('latitude')
            Lon = colourants_form.cleaned_data.get('longitude')
            con = colourants_form.cleaned_data.get('category_of_find')
            col = colourants_form.cleaned_data.get('colour')
            pig = colourants_form.cleaned_data.get('pigment')
            chrFrom = request.POST.get('chr-from')
            
            if con == 'other':
                instance.category_of_find = con_other
                instance.save()
            if col == 'other':
                instance.colour = col_other
                instance.save()    
            if pig == 'other':
                instance.pigment = pig_other
                instance.save()  
            if(chr_other):
               
                if chrFrom == 'bce':
                    instance.chronology_from = -int(chr_other)    
                    instance.chronology_to = -int(chr_other) 
                if chrFrom == 'ce': 
                    instance.chronology_from = chr_other    
                    instance.chronology_to = chr_other     
                instance.save()   
                  
            if Lat and Lon:
                location = geolocator.reverse((Lat, Lon), language='en')

                if location:
                    instance.location = location.address

                    instance.save()
                    messages.success(request, "The form has been submitted")
                else:
                    messages.error(request, "Wrong address!")

            elif loc:
                location = geolocator.geocode(loc, language='en')
                if location:
                    lat = location.latitude
                    lon = location.longitude
                    instance.latitude = lat
                    instance.longitude = lon
                    instance.location = location.address
                    instance.save()

                    messages.success(request, "The form has been submitted")
                else:
                    messages.error(request, "Wrong address!")

            else:
                messages.error(request, "You have to provide an location!")
        else:
            messages.error(request, "Sorry something went wrong try again ")

    colourants_form = ColourantsForm()
    search_form = SearchForm()
    context_other = ContextOther()
    colour_other = ColourOther()
    pigment_other  =PigmentOther()
    chronology_other = ChronologyOther()
    m = m._repr_html_()

    context = {
        'map': m,
        'c_f': colourants_form,
        'search_form': search_form,
        'context_other': context_other,
        'colour_other': colour_other,
        'pigment_other': pigment_other,
        'chronology_other': chronology_other,
    }
    return render(request, 'colors/index.html', context)


def pigments_map(request):  
    
    select_by = request.GET.get('select-by')

    chr = False
    
    if request.POST:
        if select_by == 'context':           
            
            select_colourant = ContextSelectForm(request.POST)

        elif(select_by == 'chronology_from'):
            select_colourant = ChronologySelectForm(request.POST)

        else:
            select_by = 'colour'
            select_colourant = ColourantSelectForm(request.POST)
           

        if select_colourant.is_valid():
            if select_by == 'chronology_from':
                chr = True
                period_from = select_colourant.cleaned_data['chr_select_from']
                period_to = select_colourant.cleaned_data['chr_select_to']
                chr_from = select_colourant.cleaned_data['chr_input_from']
                chr_to = select_colourant.cleaned_data['chr_input_to']
                selection = chr_format(
                    period_from, period_to, chr_from, chr_to)

            if select_by == 'colour':
                chr =True
                colour =select_colourant.cleaned_data['colour']
                pigment = select_colourant.cleaned_data['pigment']
                if colour or pigment:
                     selection = [colour,pigment] 
                else:
                    selection = None

                

            if select_by == 'context': 
                context = select_colourant.cleaned_data[select_by]
                
                if context == 'all' :  
                    
                    selection = None    
                else:
                    selection = context

            if selection:
                msg = select(select_by, selection)['msg'] 
  

                if msg :
                    m = select(select_by, selection)['map']
                    counter = select(select_by, selection)['counter']
                    colourant_list = select(select_by, selection)['colourant_list']
                    
                    if msg == 'chronology':
                        messages.error(
                        request, "No Colourants found in that period")
                    if msg == 'colour-pigment':
                        messages.error(
                        request, "No Colourants found with these characteristics")
                else:
                    
                    m = select(select_by, selection)['map']
                    counter = select(select_by, selection)['counter']
                    colourant_list = select(select_by, selection)[
                        'colourant_list']

            else:
          
                chr = False
                selection = ''
                m = select(select_by, selection)['map']
                counter = select(select_by, selection)['counter']
                colourant_list = select(select_by, selection)['colourant_list']

                if select_by == 'context':
            
                    select_colourant = ContextSelectForm()
        
                elif select_by == 'chronology_from':
                    chr = True
                    select_colourant = ChronologySelectForm()
            
                else:
                    chr = True
                    select_colourant = ColourantSelectForm();
            
            

            context = {
                'chr': chr,
                'counter': counter,
                'colourant_list': colourant_list,
                'map': m,
                'select_colourant': select_colourant,
        

            }
            return render(request, 'colors/map.html', context)


    else:

        chr = False
        selection = ''
        m = select(select_by, selection)['map']
        counter = select(select_by, selection)['counter']
        colourant_list = select(select_by, selection)['colourant_list']

        if select_by == 'context':
            
            select_colourant = ContextSelectForm()
        
        elif select_by == 'chronology_from':
            chr = True
            select_colourant = ChronologySelectForm()
            
        else:
            chr = True
            select_colourant = ColourantSelectForm();
            
            

    context = {
        'chr': chr,
        'counter': counter,
        'colourant_list': colourant_list,
        'map': m,
        'select_colourant': select_colourant,
        

    }
    return render(request, 'colors/map.html', context)


class ColourantsDetailView(generic.DetailView):
    model = Colourants


def contact_view(request):
    return render(request, 'colors/contact.html')


def help_view(request):
    return render(request, 'colors/info.html')
