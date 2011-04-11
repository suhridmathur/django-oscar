from django import forms
from haystack.forms import FacetedSearchForm
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import Input


class SearchInput(Input):
    '''
    Defining a search type widget

    This is an HTML5 thing and works nicely with Safari, other browsers default
    back to using the default "text" type
    '''
    input_type = 'search'

class MultiFacetedSearchForm(FacetedSearchForm):
    '''
    An extension of the regular faceted search form to alow for multiple facets
    '''
    q = forms.CharField(required=False, label=_('Search'), widget=SearchInput({ "placeholder": _('Search') }))

    def search(self):
        '''
        Overriding the search method to allow for multiple facets
        '''
        sqs = super(FacetedSearchForm, self).search().order_by('-date_updated')
        if hasattr(self, 'cleaned_data') and self.cleaned_data['selected_facets']:
            for f in self.cleaned_data['selected_facets'].split("|"):
                sqs = sqs.narrow(f)
        return sqs