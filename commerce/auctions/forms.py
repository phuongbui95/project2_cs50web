from django import forms
from .models import Listing, Category

class CreateListingForm(forms.ModelForm):
    # Admin will create Categories in advance in Admin site so that users can select
    ###--- if there is no value in the database at the beginning, error: no matching querry
    # category = forms.ModelChoiceField(queryset=Category.objects.all(),
    #                                   initial=Category.objects.get(category_name='Other')
    #                                   )
    class Meta:
        model = Listing
        fields = ['category', 'title', 'description', 'price', 'image']