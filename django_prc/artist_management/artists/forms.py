from django import forms
from .models import Artists

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artists
        fields = ['name', 'dob', 'gender', 'address', 'first_release_year', 'no_of_albums_released']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
