from django import forms
from .models import FlashCard

# Creating the form class
class FlashCardForm(forms.ModelForm):

    title = forms.CharField(required=False)

    class Meta:
        model = FlashCard
        fields = ('title', 'frontface', 'backface',
                    'know_level', 'activated')
        
        ##  Adding widgets for later styling
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-title'}),
            'frontface':forms.Textarea(attrs={'class':'form-text medium-editor-textarea'}),
            'backface':forms.Textarea(attrs={'class':'form-text medium-editor-textarea'}),
            'know_level':forms.NumberInput(attrs={'class':'know_level'}),
            'activated':forms.CheckboxInput(attrs={'class':'activated'}),
        }
        