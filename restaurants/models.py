from django.db import models
from django.contrib.auth.models import User
from management.models import AssistantModel
from django.core.exceptions import ValidationError
import json
from zoneinfo import available_timezones
from zoneinfo import ZoneInfo

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
    
class Restaurant(models.Model):
    owner = models.ForeignKey(Customer, related_name='restaurants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    # Create a list of common timezone choices
    TIMEZONE_CHOICES = [
        ('Europe/Budapest', 'Budapest (Hungary)'),
        ('Europe/London', 'London'),
        ('Europe/Paris', 'Paris'),
    ] # add more it is needed
    
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES,
        default='Europe/Budapest'
    )
    assistant = models.ForeignKey(AssistantModel, related_name='restaurants', on_delete=models.CASCADE, null=True)
    opening_hours = models.OneToOneField('OpeningHours', related_name='restaurant_hours', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name

    def get_timezone(self):
        return ZoneInfo(self.timezone)
    
    
class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='tables', on_delete=models.CASCADE)
    table_id = models.CharField(max_length=20)
    capacity = models.IntegerField()
    
class OpeningHours(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    restaurant = models.OneToOneField('Restaurant', related_name='hours', on_delete=models.CASCADE)
    hours = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = "Opening Hours"

    def __str__(self):
        return f"Opening Hours for {self.restaurant.name}"

    def set_hours(self, day, slots):
        
        """
        example: 
        monday_slots = [
                {'start': '09:00', 'end': '12:00'},
                {'start': '12:00', 'end': '15:00'},
                {'start': '18:00', 'end': '22:00'}
            ]
            opening_hours.set_hours('monday', monday_slots)
        """
        if day not in dict(self.DAYS_OF_WEEK):
            raise ValueError("Invalid day")
        
        for slot in slots:
            if 'start' not in slot or 'end' not in slot:
                raise ValueError("Each slot must have 'start' and 'end' times")
        
        current_hours = self.hours.copy()
        current_hours[day] = slots
        self.hours = current_hours
        self.save()
        print('Saved!')

    def get_hours(self, day):
        return self.hours.get(day, [])

    def is_open_at(self, datetime):
        
        """
        is_open = opening_hours.is_open_at(datetime(2024, 9, 20, 13, 30))  # Check if open on Sept 9, 2024  13:30
        print(f"Restaurant is {'open' if is_open else 'closed'} at the specified time.")
        
        """
        day = datetime.strftime('%A').lower()
        time = datetime.time()
        day_slots = self.get_hours(day)
        
        for slot in day_slots:
            start = self.parse_time(slot['start'])
            end = self.parse_time(slot['end'])
            if start <= time < end:
                return True
        return False

    @staticmethod
    def parse_time(time_str):
        from datetime import datetime
        return datetime.strptime(time_str, "%H:%M").time()

    def clean(self):
        for day, slots in self.hours.items():
            if day not in dict(self.DAYS_OF_WEEK):
                raise ValidationError(f"Invalid day: {day}")
            for slot in slots:
                if 'start' not in slot or 'end' not in slot:
                    raise ValidationError(f"Invalid slot for {day}: {slot}")
                start = self.parse_time(slot['start'])
                end = self.parse_time(slot['end'])
                if start >= end:
                    raise ValidationError(f"End time must be after start time for {day}: {slot}")

    def get_hours_for_day(self, day_name):
        start = getattr(self, f'{day_name.lower()}_start')
        end = getattr(self, f'{day_name.lower()}_end')
        if start and end:
            return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"
        return "Closed"

class Reservation(models.Model): # TODO: We need to check query date is avaliablty for the table.
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    restaurant = models.ForeignKey(Restaurant, related_name='reservations', on_delete=models.CASCADE)
    table = models.ForeignKey(Table, related_name='reservations', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    party_size = models.IntegerField()
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES) # custo
    notes = models.TextField(blank=True) # take note from the content of the call.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Subscription(models.Model): #TODO
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    customer = models.ForeignKey(Customer, related_name='subscriptions', on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Billing(models.Model):#TODO
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]
    customer = models.ForeignKey(Customer, related_name='billings', on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, related_name='billings', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


