from django import forms
from .models import Restaurant, Table, OpeningHours, Reservation

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'timezone']
    
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.owner:
            instance.owner = self.owner
        if commit:
            instance.save()
        return instance

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['table_id', 'capacity']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'start_time', 'end_time', 'party_size']

    def __init__(self, *args, **kwargs):
        self.restaurant = kwargs.pop('restaurant', None)
        super().__init__(*args, **kwargs)
        if self.restaurant:
            self.fields['table'].queryset = Table.objects.filter(restaurant=self.restaurant)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.restaurant:
            instance.restaurant = self.restaurant
        if commit:
            instance.save()
        return instance
    
    

class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ['restaurant', 'hours']
        widgets = {
            'hours': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.day_fields = {}

        for day, day_name in OpeningHours.DAYS_OF_WEEK:
            self.day_fields[day] = []
            
            for i in range(3):  # Assuming a maximum of 3 slots per day
                start_field = forms.TimeField(
                    required=False,
                    widget=forms.TimeInput(attrs={'type': 'time'}),
                    label=f"{day_name} Start {i+1}"
                )
                end_field = forms.TimeField(
                    required=False,
                    widget=forms.TimeInput(attrs={'type': 'time'}),
                    label=f"{day_name} End {i+1}"
                )
                
                self.fields[f'{day}_start_{i}'] = start_field
                self.fields[f'{day}_end_{i}'] = end_field
                self.day_fields[day].append((start_field, end_field))

    def clean(self):
        cleaned_data = super().clean()
        hours = {}

        for day, day_name in OpeningHours.DAYS_OF_WEEK:
            day_slots = []
            for i, (start_field, end_field) in enumerate(self.day_fields[day]):
                start = cleaned_data.get(f'{day}_start_{i}')
                end = cleaned_data.get(f'{day}_end_{i}')
                
                if start and end:
                    if start >= end:
                        self.add_error(f'{day}_start_{i}', "End time must be after start time")
                    else:
                        day_slots.append({
                            'start': start.strftime('%H:%M'),
                            'end': end.strftime('%H:%M')
                        })
                elif start or end:
                    self.add_error(f'{day}_start_{i}', "Both start and end times must be provided")
            
            if day_slots:
                hours[day] = day_slots

        cleaned_data['hours'] = hours
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.hours = self.cleaned_data['hours']
        if commit:
            instance.save()
        return instance