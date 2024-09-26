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
        fields = ['restaurant']
        widgets = {
            'hours': forms.HiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.day_fields = {}

        for day, day_name in OpeningHours.DAYS_OF_WEEK:
            self.day_fields[day] = []
            self.fields[f'{day}_start_0'] = forms.TimeField(
                required=False,
                widget=forms.TimeInput(attrs={'type': 'time'}),
                label=f"{day_name} start 0"
            )
            self.fields[f'{day}_end_0'] = forms.TimeField(
                required=False,
                widget=forms.TimeInput(attrs={'type': 'time'}),
                label=f"{day_name} end 0"
            )

        if self.instance.pk and self.instance.hours:
            for day, slots in self.instance.hours.items():
                for i, slot in enumerate(slots):
                    self.fields[f'{day}_start_{i}'].initial = slot['start']
                    self.fields[f'{day}_end_{i}'].initial = slot['end']

    def clean(self):
        cleaned_data = super().clean()
        hours = {}
        for day, day_name in OpeningHours.DAYS_OF_WEEK:
            day_slots = []
            slot_index = 0
            while True:
                start = cleaned_data.get(f'{day}_start_{slot_index}')
                end = cleaned_data.get(f'{day}_end_{slot_index}')

                if not start and not end:
                    break  # No more slots for this day
                
                if start and end:
                    if start >= end:
                        self.add_error(f'{day}_start_{slot_index}', "End time must be after start time")
                    else:
                        day_slots.append({
                            'start': start.strftime('%H:%M'),
                            'end': end.strftime('%H:%M')
                        })
                elif start or end:
                    self.add_error(f'{day}_start_{slot_index}', "Both start and end times must be provided")
                
                slot_index += 1
            
            if day_slots:
                hours[day] = day_slots

        cleaned_data['hours'] = hours
        print(cleaned_data['hours'])
        return cleaned_data

    def save(self, commit=True):
        print('here')
        instance = super().save(commit=False)
        
        instance.set_hours(self.clean()['hours'])
        
        if commit:
            instance.save()
        return instance