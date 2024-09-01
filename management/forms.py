from django import forms
from .models import Assistant

class AssistantForm(forms.ModelForm):
    class Meta:
        model = Assistant
        fields = '__all__'  # Include all fields from the model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize the form fields here if needed
        self.fields['created_at'].widget = forms.HiddenInput()
        self.fields['updated_at'].widget = forms.HiddenInput()
