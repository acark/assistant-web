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
    
from datetime import datetime, time
class OpeningHoursForm(forms.ModelForm):
    
    class Meta:
        model = OpeningHours
        fields = ['restaurant']
        # widgets = {
        #     'hours': forms.HiddenInput(),
        # }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for day, day_name in OpeningHours.DAYS_OF_WEEK:
            self.fields[f'{day}_closed'] = forms.BooleanField(required=False, label=f"{day} closed", initial=True)

            for i in range(7): # assuming max 7 slots per day
                self.fields[f'{day}_start_{i}'] = forms.TimeField(
                    required=False,
                    widget=forms.TimeInput(attrs={'type': 'time'}),
                    label=f"{day_name} start {i}",
                    initial= '15:00'
                )
                
                self.fields[f'{day}_end_{i}'] = forms.TimeField(
                    required=False,
                    widget=forms.TimeInput(attrs={'type': 'time'}),
                    label=f"{day_name} end {i}",
                    initial = '19:00'
                )
                
        if self.instance.pk:  # Check if updating an existing instance
            for day, slots in self.instance.hours.items():
                if slots[0] == 'closed':
                    self.fields[f'{day}_closed'].initial = True  # Checkbox should be checked
                elif isinstance(slots, list) and slots[0] != 'closed':
                    self.fields[f'{day}_closed'].initial = False  # Checkbox should be unchecked
                    for i, slot in enumerate(slots):
                        if isinstance(slot, dict) and 'start' in slot and 'end' in slot:
                            self.fields[f'{day}_start_{i}'].initial = slot['start']
                            self.fields[f'{day}_end_{i}'].initial = slot['end']
                        else:
                            # Handle unexpected slot structure
                            self.fields[f'{day}_start_{i}'].initial = None
                            self.fields[f'{day}_end_{i}'].initial = None
                            raise ValueError

    def clean(self):
        cleaned_data = super().clean()
        hours = {}
        closed_days = []
        for field_name, value in cleaned_data.items():
            if field_name == "restaurant" or not value: continue
            
            if field_name.endswith('_closed'):
                day = field_name[:-7]  # Remove '_closed' from the end
                if value:  # If closed is True
                    closed_days.append(day)
                    continue
            if field_name.split('_')[0] in closed_days:
                continue
            
            day, slot_type, slot_num = field_name.rsplit('_', 2)
            slot_num = int(slot_num)
            if day not in hours:
                hours[day] = []
                
                
            while len(hours[day]) <= slot_num:
                hours[day].append({'start': None, 'end': None})
            
            hours[day][slot_num][slot_type] = value.strftime('%H:%M')
            
              
         # Remove empty slots
        for day in hours:
            if day in closed_days:
                hours[day] = ['closed']
            else:
                hours[day] = [slot for slot in hours[day] if slot['start'] and slot['end']]

        cleaned_data['hours'] = hours
    
        return cleaned_data

    def save(self, commit=True):
        
        instance = super().save(commit=False)

        if commit:
            instance.save()
            instance.update_hours_from_cleaned_data(self.cleaned_data)
        return instance