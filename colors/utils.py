from colors.models import Colourants
from folium.plugins import MarkerCluster
import folium


def format_number(n):

    return n.split('/')


def chr_format(period_from, period_to, chr_from, chr_to):
    if period_from == 'bce':
        chr_f = 0 - chr_from
    else:
        chr_f = chr_from
    if period_to == 'bce':
        chr_t = 0 - chr_to
    else:
        chr_t = chr_to
    return {'chr_from': chr_f, 'chr_to': chr_t}


def map_generator(Lat, Lon, Loc, Col,Pig, selection):
    # for chronology
    if (type(selection) == dict):
        
        period_from = 'BCE' if selection['chr_from'] < 0 else 'CE'
        period_to = 'BCE' if selection['chr_to'] < 0 else 'CE'
        counter = Col.count(), "colourants found from {} {} to {} {}  period".format(
            abs(selection['chr_from']), period_from, abs(selection['chr_to']), period_to)
    else:
    
        counter = Col.count(), selection, "found"
        counter = str(counter).replace("(", "").replace(")","").replace("'", "").replace(",", "")
    marker_c = MarkerCluster()
    kw = {"prefix": "fa", "color": 'darkblue', "icon": "connectdevelop"}
    for lt, ln, lc, col,pig in zip(Lat, Lon, Loc, Col,Pig):

        html = f"""
                <h5 style="margin:1.5px; color:#232323;">Colour:</h5>{col}
                <h5 style="margin:1.5px; color:#232323;">Pigment:</h5>{pig}
                <h5 style="margin:1.5px; color:#232323;">Location:</h5>{lc}
                </*>
                """
        folium.Marker(location=[lt, ln], popup=html,icon=folium.Icon(**kw)).add_to(marker_c)
        m = folium.Map(zoom_start=2, min_zoom=2, location=[lt, ln]).add_child(marker_c)
    m = m._repr_html_()

    return {'map': m, 'counter': counter}


def not_selection(select_by):
    
    if not select_by:
        select_by = 'colour'
    selection = ''
    colourant_list = Colourants.objects.all().filter(
        check=True).order_by('pigment')
      
    Lat = Colourants.objects.filter(
        check=True).values_list('latitude', flat=True)
    Lon = Colourants.objects.filter(
        check=True).values_list('longitude', flat=True)
    Loc = Colourants.objects.filter(
        check=True).values_list('location', flat=True)
    Col = Colourants.objects.filter(
        check=True).values_list('colour', flat=True)
    Pig = Colourants.objects.filter(
        check=True, ).values_list('pigment', flat=True)
    m = map_generator(Lat, Lon, Loc, Col,Pig, selection)['map']
    counter = map_generator(Lat, Lon, Loc, Col,Pig, ('colourants'))['counter']
    msg = None
    return {'map': m, 'counter': counter, 'colourant_list': colourant_list, 'msg': msg}


def select(select_by, selection):
    msg = None  
    

    if select_by == 'colour' and selection :
        
        
        colour =selection[0]
        pigment = selection[1]
        if  colour and not pigment:
           
            Lat = Colourants.objects.filter(
                check=True, colour=colour).values_list('latitude', flat=True)
            Lon = Colourants.objects.filter(
                check=True, colour=colour).values_list('longitude', flat=True)
            Loc = Colourants.objects.filter(
                check=True, colour=colour).values_list('location', flat=True)
            Col = Colourants.objects.filter(
                check=True, colour=colour).values_list('colour', flat=True)
            colourant_list = Colourants.objects.all().filter(check=True, colour=colour, ).order_by('pigment')
            Pig = Colourants.objects.filter(
                check=True, colour=colour).values_list('pigment', flat=True)
            m = map_generator(Lat, Lon, Loc, Col,Pig, colour)['map']
            counter = map_generator(Lat, Lon, Loc, Col,Pig, colour)['counter']
       
        if  pigment and not colour:
            
            Lat = Colourants.objects.filter(
                check=True, pigment=pigment).values_list('latitude', flat=True)
            Lon = Colourants.objects.filter(
                check=True, pigment=pigment).values_list('longitude', flat=True)
            Loc = Colourants.objects.filter(
                check=True, pigment=pigment).values_list('location', flat=True)
            Col = Colourants.objects.filter(
                check=True, pigment=pigment).values_list('colour', flat=True)
            Pig = Colourants.objects.filter(
                check=True, pigment=pigment ).values_list('pigment', flat=True)
            colourant_list = Colourants.objects.all().filter(check=True, pigment=pigment, ).order_by('pigment')      
            
            m = map_generator(Lat, Lon, Loc, Col,Pig, pigment)['map']
            counter = map_generator(Lat, Lon, Loc, Col,Pig, pigment)['counter']

        if colour and pigment :
           
            Lat = Colourants.objects.filter(
                check=True, colour=colour, pigment=pigment).values_list('latitude', flat=True)
            Lon = Colourants.objects.filter(
                check=True, colour=colour, pigment=pigment).values_list('longitude', flat=True)
            Loc = Colourants.objects.filter(
                check=True, colour=colour, pigment=pigment).values_list('location', flat=True)
            Col = Colourants.objects.filter(
                check=True, colour=colour, pigment=pigment).values_list('colour', flat=True)
            Pig = Colourants.objects.filter(
                check=True,colour=colour, pigment=pigment).values_list('pigment', flat=True)
    
            if not Lat:
               
                msg = 'colour-pigment'
                m = not_selection(select_by)['map']
                counter = not_selection(select_by)['counter']
                colourant_list = not_selection(select_by)['colourant_list']        
        
            else:
                colourant_list = Colourants.objects.all().filter(check=True,pigment=pigment,colour=colour ).order_by('pigment')
                m = map_generator(Lat, Lon, Loc, Col,Pig, pigment)['map']
                counter = map_generator(Lat, Lon, Loc, Col,Pig, (colour, pigment))['counter']

        
        
    if select_by == 'context' and selection:
        selection = selection[0]
        colourant_list = Colourants.objects.all().filter(check=True, context=selection).order_by('pigment')
        
        Lat = Colourants.objects.filter(
            check=True, context=selection).values_list('latitude', flat=True)
        Lon = Colourants.objects.filter(
            check=True, context=selection).values_list('longitude', flat=True)
        Loc = Colourants.objects.filter(
            check=True, context=selection).values_list('location', flat=True)
        Col = Colourants.objects.filter(
            check=True, context=selection).values_list('colour', flat=True)
        Pig = Colourants.objects.filter(
            check=True,context=selection).values_list('pigment', flat=True)
        
        m = map_generator(Lat, Lon, Loc, Col,Pig, selection)['map']
        counter = map_generator(Lat, Lon, Loc, Col,Pig, selection)['counter']
    
    if select_by == 'chronology_from' and selection:
        

        colourant_list = Colourants.objects.all().filter(
            check=True, chronology_from__range=(selection['chr_from'], selection['chr_to']), chronology_to__range=(selection['chr_from'], selection['chr_to'])).order_by('pigment')
        Lat = Colourants.objects.filter(
            check=True, chronology_from__range=(selection['chr_from'], selection['chr_to']), chronology_to__range=(selection['chr_from'], selection['chr_to'])).values_list('latitude', flat=True)
        Lon = Colourants.objects.filter(
            check=True, chronology_from__range=(selection['chr_from'], selection['chr_to']), chronology_to__range=(selection['chr_from'], selection['chr_to'])).values_list('longitude', flat=True)
        Loc = Colourants.objects.filter(
            check=True, chronology_from__range=(selection['chr_from'], selection['chr_to']), chronology_to__range=(selection['chr_from'], selection['chr_to'])).values_list('location', flat=True)
        Col = Colourants.objects.filter(
            check=True, chronology_from__range=(selection['chr_from'], selection['chr_to']), chronology_to__range=(selection['chr_from'], selection['chr_to'])).values_list('colour', flat=True)
        Pig = Colourants.objects.filter(
            check=True, chronology_from__range=(selection['chr_from'], selection['chr_to']), chronology_to__range=(selection['chr_from'], selection['chr_to'])).values_list('colour', flat=True).values_list('pigment', flat=True)
        if not Lat:
            msg = 'chronology'
            m = not_selection(select_by)['map']
            counter = not_selection(select_by)['counter']
            colourant_list = not_selection(select_by)['colourant_list']

        else:
            m = map_generator(Lat, Lon, Loc, Col,Pig, selection)['map']
            counter = map_generator(Lat, Lon, Loc, Col,Pig, selection)['counter']

    if not selection:
        
        m = not_selection(select_by)['map']
        counter = not_selection(select_by)['counter']
        colourant_list = not_selection(select_by)['colourant_list']
        msg = not_selection(select_by)['msg']

    return {'map': m, 'counter': counter, 'colourant_list': colourant_list, 'msg': msg}
