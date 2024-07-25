from django import forms
from .models import Criterion, Project

class RatingForm(forms.ModelForm):
    class Meta:
        model = Criterion
        fields = ['rating', 'gewichtung']
        widgets = {
            'rating': forms.RadioSelect(choices=Criterion.RATING_CHOICES),
            'gewichtung': forms.Select(choices=Criterion.WEIGHT_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        self.fields['gewichtung'].initial = 1  
        self.fields['gewichtung'].choices = Criterion.WEIGHT_CHOICES  

        # Entfernen Sie die leere Wahlmöglichkeit für das Bewertungsfeld
        self.fields['rating'].choices = [
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (0, 'Nicht relevant')
        ]  
    
    # def __init__(self, *args, **kwargs):
    #     super(RatingForm, self).__init__(*args, **kwargs)
    #     self.fields['gewichtung'].initial = 1  # Standardwert für Gewichtung (z.B. 'Einfach')
    #     self.fields['gewichtung'].empty_label = None  # Entfernt die --------- Option
    #     self.fields['rating'].empty_label = None  # Entfernt die --------- Option für rating

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name'] 