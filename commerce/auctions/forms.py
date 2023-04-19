from django import forms
from .models import Listing, Category

class CreateListingForm(forms.ModelForm):
    # Admin will create Categories in advance in Admin site so that users can select
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      initial=Category.objects.get(category_name='Other')
                                      )
                                    
    
    class Meta:
        model = Listing
        fields = ['category', 'title', 'description', 'price', 'image']
        