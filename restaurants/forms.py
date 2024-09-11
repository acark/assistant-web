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

class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ['day', 'open_time', 'close_time']

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