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
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'frontface':forms.Textarea(attrs={'class':'frontface medium-editor-textarea'}),
            'backface':forms.Textarea(attrs={'class':'backface medium-editor-textarea'}),
            'know_level':forms.NumberInput(attrs={'class':'know_level'}),
            'activated':forms.CheckboxInput(attrs={'class':'activated'}),
        }
        