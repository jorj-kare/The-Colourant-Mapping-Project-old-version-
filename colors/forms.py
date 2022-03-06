
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH, CharField, DecimalField, TextField
from .models import Colourants
from django.forms.widgets import CheckboxInput, EmailInput, NumberInput, TextInput, Textarea, Select
from django.utils.translation import ugettext_lazy as _


class ColourantsForm(forms.ModelForm):

    class Meta:
        model = Colourants

        exclude = (
            'created_date',
            'check'

        )
        CHOICES_CONTEXT = (('', 'Select category of find'), ('wall painting', 'Wall painting'), ("sculpture", "Sculpture"),
                           ("pottery", "Pottery"), ("unused pigment", "Unused pigment"),("dyestuff", "Dyestuff"), ("deposit", "Deposit"), ("other", "Other"))

        CHOICES = (('BCE', (('', 'Select Chronology'),(-5000, '5000'),
                            (-4000, "4000"), (-3000,
                                                            "3000"),
                            (-2000, "2000"), (-1000,
                                                            "1000"),
                            (-900, "900"), (-800, '800'),
                            (-700, "700"), (-600, "600"),
                            (-500, "500"), (-400, "400"),
                            (-300, "300"), (-200, "200"),
                            (-100, "100"),
                            (0, "0"))), ('CE', (
                                ('', 'Select Chronology'),
                                (0, "0"),
                                (100, "100"), (200, "200"),
                                (300, "300"), (400, "400"),
                                (500, "500"), (600, "600"),
                                (700, "700"), (800, "800"),
                                (900, "900"), (1000, "1000"))),)

        PIGMENT_CHOICES=(('','Select pigment'),('azurite','Azurite'),('brown ochre','Brown ochre'),('calcium carbonate','Calcium carbonate'),('calcium sulfate','Calcium sulfate'),('charcoal','Charcoal'),('cinnabar','Cinnabar'),('copper salts','Copper salts'),('Egyptian blue','Egyptian blue'),('Egyptian green','Egyptian green'),('galena','Galena'),('green earth (celadonite)','Green earth (Celadonite)'),('green earth (glauconite)','Green earth (Glauconite)'),('Han blue','Han blue'),('Han purple','Han purple'),('huntine','Huntine'),('indigo','Indigo'),('kaolinite','Kaolinite'),('kermes','Kermes'),('lazurite','Lazurite'),('lead white','Lead white'),('madder','Madder'),('malachite','Malachite'),('manganese oxide','Manganese oxide'),('Maya blue','Maya blue'),('murex purple','Murex purple'),('orpiment','Orpiment'),('realgar','Realgar'),('red lead','Red lead'),('red earth','Red earth'),('soot','Soot'),('verdigris','Verdigris'),('yellow earth','Yellow earth'),('other','Other'))
        
        
        COLOUR_CHOICES=(('','Select colour'),('red','Red'),('brown','Brown'),('yellow','Yellow'),('green','Green'),('blue','Blue'),('purple','Purple'),('black','Black'),('white','White'),('other','Other'))

        widgets = {
            'pigment': Select(choices = PIGMENT_CHOICES ,attrs={'placeholder': 'e.g. Egyptian blue, red earth',}),
            'colour': Select(choices = COLOUR_CHOICES ,attrs={'placeholder': 'e.g. Red, Blue'}),
            'chronology_from': Select(choices=CHOICES, attrs={'placeholder': 'e.g. 5th century BCE'}),
            'chronology_to': Select(choices=CHOICES, attrs={'placeholder': 'e.g. 5th century BCE'}),
            'archeological_context': Textarea(attrs={'rows': 2, 'placeholder': 'Provide additional information about the context of the finds if needed.'}),
            'category_of_find': Select(
                choices=CHOICES_CONTEXT, attrs={'class': 'context_select'}),
            'references': Textarea(attrs={'rows': 3, 'placeholder': 'Relevant publications.'}),
            'notes': Textarea(attrs={'rows': 2, 'placeholder': 'Extra space to provide additional information or clarifications for your entry.'}),
            'latitude': NumberInput(),
            'longitude': NumberInput(),
            'location': TextInput(attrs={'placeholder': 'e.g. Rome, Italy '}),
            'name': TextInput(attrs={'placeholder': 'Name and Surname'}),
            'email': EmailInput(attrs={'placeholder': 'pliny@naturalishistoria.com'}),
            'affiliation': Textarea(attrs={'rows': 1, 'placeholder': 'Please, enter your affiliation, if applicable. '}),
            'techniques': Textarea(attrs={'rows': 2, 'placeholder':'Provide a list of the analytical techniques used for the identification of the pigment.'}),
            'publicly_available': CheckboxInput(),
            'check': CheckboxInput(),

        }

        labels = {
            'techniques': _('Analytical Techniques'),
            'publicly_available': 'Publicly available information',
            'pigment' : '',
            'colour' : '',

        }

        # help_texts = {
        #     'publicly_available': "Check this box if you would like your personal info (name and affiliation) to be published. ",
        # }


class SearchForm(forms.Form):
    find = forms.CharField(max_length=100, required=False, label='',   widget=forms.TextInput(
        attrs={'placeholder': 'Search for a place'}))






class ColourOther(forms.Form):
    colour_other = forms.CharField(
        max_length=100, required=False, label='',   widget=forms.Textarea(attrs={'class': 'colour_other', 'rows': 2, 'placeholder': 'Other: please specify.'}))

class ContextOther(forms.Form):
    context_other = forms.CharField(
        max_length=100, required=False, label='',   widget=forms.Textarea(attrs={'class': 'context_other', 'rows': 2, 'placeholder': 'Other: please specify.'}))

class PigmentOther(forms.Form):
    pigment_other = forms.CharField(
        max_length=100, required=False, label='',   widget=forms.Textarea(attrs={'class': 'pigment_other', 'rows': 2, 'placeholder': 'Other: please specify.'}))
class ChronologyOther(forms.Form):
    chronology_other = forms.IntegerField(label='Specific date',widget=NumberInput(attrs={'class': 'chronology_other'}))

CHOICES_PERIOD = (('bce', 'BCE'), ('ce', 'CE'))

# map Section
class ChronologySelectForm(forms.Form):
    chr_select_from = forms.ChoiceField(
        choices=CHOICES_PERIOD, required=False, label='', widget=forms.Select(attrs={'class': 'search__period'}))
    chr_input_from = forms.IntegerField(
        required=True, label='', widget=NumberInput(attrs={'class': 'search__chronology'}))
    chr_select_to = forms.ChoiceField(
        choices=CHOICES_PERIOD,  required=False, label='',  widget=forms.Select(attrs={'class': 'search__period'}))
    chr_input_to = forms.IntegerField(
        required=True, label='', widget=NumberInput(attrs={'class': 'search__chronology'}))

        
def context():
    return[("all", "All categories of find")] + list(Colourants.objects.values_list('category_of_find', 'category_of_find').filter(check=True).distinct())


class ContextSelectForm(forms.Form):
    context = forms.ChoiceField(
        choices=context, widget=forms.Select(attrs={'onchange': 'this.form.submit();'}), required=False, label='')



def unique_colours():
    return[("", "All Colours")] + list(Colourants.objects.values_list('colour', 'colour').filter(check=True).distinct())
 
def unique_pigments():
    return[("", "All Pigments")] + list(Colourants.objects.values_list('pigment', 'pigment').filter(check=True).distinct())


class ColourantSelectForm(forms.Form):
    colour = forms.ChoiceField(
        choices=unique_colours,  widget=forms.Select(attrs={'class': 'colour-map' }), required=False, label='')

    pigment = forms.ChoiceField(
        choices=unique_pigments,  widget=forms.Select(attrs={'class': 'pigment-map'}), required=False, label='')


