
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
        CHOICES_CONTEXT = (('', 'Select context'), ('wall painting', 'Wall painting'), ("sculpture", "sculpture"),
                           ("pottery", "Pottery"), ("raw pigment", "Raw pigment"), ("lump", "Lump"), ("deposit", "Deposit"), ("other", "Other"))

        CHOICES = (('BCE', ((-5000, '5th millennium BCE'),
                            (-4000, "4th millennium BCE"), (-3000,
                                                            "3th millennium BCE"),
                            (-2000, "2th millennium BCE"), (-1000,
                                                            "1st millennium BCE"),
                            (-900, "9th century BCE"), (-800, '8th century BCE'),
                            (-700, "7th century BCE"), (-600, "6th century BCE"),
                            (-500, "5th century BCE"), (-400, "4th century BCE"),
                            (-300, "3th century BCE"), (-200, "2th century BCE"),
                            (-100, "1st century BCE"))), ('CE', (
                                (100, "1st century CE"), (200, "2th century CE"),
                                (300, "3th century CE"), (400, "4th century CE"),
                                (500, "5th century CE"), (600, "6th century CE"),
                                (700, "7th century CE"), (800, "8th century CE"),
                                (900, "9th century CE"), (1000, "10th century CE"))),)

        PIGMENT_CHOICES=(('','Select pigment'),('red earth','Red earth'),('cinnabar','Cinnabar'),('red lead','Red lead'),('kermes','Kermes'),('sandarach (realgar)','Sandarach (Realgar)'),('madder','Madder'),('yellow earth','Yellow earth'),('orpiment','Orpiment'),('malachite','Malachite'),('verdigris','Verdigris'),('other','Other'))
        COLOUR_CHOICES=(('','Select colour'),('red','Red'),('brown','Brown'),('yellow','Yellow'),('green','Green'),('blue','Blue'),('purple','Purple'),('black','Black'),('white','White'),('other','Other'))

        widgets = {
            'pigment': Select(choices = PIGMENT_CHOICES ,attrs={'placeholder': 'e.g. Egyptian blue, red earth',}),
            'colour': Select(choices = COLOUR_CHOICES ,attrs={'placeholder': 'e.g. Red, Blue'}),
            'chronology_from': Select(choices=CHOICES, attrs={'placeholder': 'e.g. 5th century BCE'}),
            'chronology_to': Select(choices=CHOICES, attrs={'placeholder': 'e.g. 5th century BCE'}),
            'archeological_context': Textarea(attrs={'rows': 2, 'placeholder': 'Provide additional information about the context of the finds if needed.'}),
            'context': Select(
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
    return[("", "All Contexts")] + list(Colourants.objects.values_list('context', 'context').filter(check=True).distinct())


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


