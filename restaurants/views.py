from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from .models import Customer, Restaurant, Table, OpeningHours, Reservation, Subscription, Billing
from .forms import OpeningHoursForm

from django.contrib import messages

# Customer Views
class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customer_detail.html'
    context_object_name = 'customer'

class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'customer_form.html'
    fields = ['user', 'phone_number', 'address']
    success_url = reverse_lazy('customer-list')

class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'customer_form.html'
    fields = ['phone_number', 'address']
    success_url = reverse_lazy('customer-list')

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')

# Restaurant Views
class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'
    context_object_name = 'restaurants'

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'
    context_object_name = 'restaurant'

class RestaurantCreateView(CreateView):
    model = Restaurant
    template_name = 'restaurant_form.html'
    fields = ['owner', 'name', 'timezone', 'assistant']
    success_url = reverse_lazy('restaurant-list')

class RestaurantUpdateView(UpdateView):
    model = Restaurant
    template_name = 'restaurant_form.html'
    fields = ['name', 'timezone', 'assistant']
    success_url = reverse_lazy('restaurant-list')

class RestaurantDeleteView(DeleteView):
    model = Restaurant
    template_name = 'restaurant_confirm_delete.html'
    success_url = reverse_lazy('restaurant-list')

# Table Views
class TableListView(ListView):
    model = Table
    template_name = 'table_list.html'
    context_object_name = 'tables'

class TableDetailView(DetailView):
    model = Table
    template_name = 'table_detail.html'
    context_object_name = 'table'

class TableCreateView(CreateView):
    model = Table
    template_name = 'table_form.html'
    fields = ['restaurant', 'table_id', 'capacity']
    success_url = reverse_lazy('table-list')

class TableUpdateView(UpdateView):
    model = Table
    template_name = 'table_form.html'
    fields = ['table_id', 'capacity']
    success_url = reverse_lazy('table-list')

class TableDeleteView(DeleteView):
    model = Table
    template_name = 'table_confirm_delete.html'
    success_url = reverse_lazy('table-list')

# OpeningHours Views
class OpeningHoursListView(ListView):
    model = OpeningHours
    template_name = 'opening_hours_list.html'
    context_object_name = 'opening_hours'
    paginate_by = 10

    def get_queryset(self):
        queryset = OpeningHours.objects.select_related('restaurant').all()
        print(queryset)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(Q(restaurant__name__icontains=search_query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context
    
    
    
class OpeningHoursDetailView(DetailView):
    model = OpeningHours
    template_name = 'opening_hours_detail.html'
    context_object_name = 'opening_hours'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opening_hours = self.object

        # Create a list of days with their corresponding hours
        days_hours = []
        for day, day_name in OpeningHours.DAYS_OF_WEEK:
            hours = opening_hours.hours.get(day, [])

            if isinstance(hours, str) and hours == "closed":  # Check if hours is a string and equals "closed"
                days_hours.append({
                    'day': day_name,
                    'hours': ['Closed']
                })
            elif isinstance(hours, list):  # Ensure hours is a list before processing
                if not hours:  # Check if the list is empty
                    days_hours.append({
                        'day': day_name,
                        'hours': ['Closed']
                    })
                else:
                    formatted_hours = []
                    for slot in hours:
                        if isinstance(slot, dict) and 'start' in slot and 'end' in slot:
                            formatted_hours.append(f"{slot['start']} - {slot['end']}")
                    days_hours.append({
                        'day': day_name,
                        'hours': formatted_hours or ['Closed']
                    })
            else:
                days_hours.append({
                    'day': day_name,
                    'hours': ['Closed']  # Fallback for unexpected cases
                })
        
        context['days_hours'] = days_hours
        return context

class OpeningHoursCreateView(CreateView):
    model = OpeningHours
    form_class = OpeningHoursForm
    template_name = 'opening_hours_form.html'
    success_url = reverse_lazy('opening-hours-list')
    def get_initial(self):
        initial = super().get_initial()
        if self.object:
            for day, slots in self.object.hours.items():
                for i, slot in enumerate(slots):
                    initial[f'{day}_start_{i}'] = slot['start']
                    initial[f'{day}_end_{i}'] = slot['end']
        return initial
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Opening hours created successfully.')
            return response
        except Exception as e:
            messages.error(self.request, f'An error occurred: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error creating the opening hours')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class OpeningHoursUpdateView(UpdateView):
    model = OpeningHours
    form_class = OpeningHoursForm
    template_name = 'opening_hours_form.html'
    success_url = reverse_lazy('opening-hours-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Opening hours updated successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating the opening hours.')
        return super().form_invalid(form)
    def get_initial(self):
        initial = super().get_initial()
        if self.object:
            for day, slots in self.object.hours.items():
                if slots == 'closed':
                    initial[f'{day}_closed'] = True
                elif isinstance(slots, list):  # Ensure slots is a list
                    initial[f'{day}_closed'] = False  # Set to False if not closed
                    for i, slot in enumerate(slots):
                        if isinstance(slot, dict) and 'start' in slot and 'end' in slot:
                            initial[f'{day}_start_{i}'] = slot['start']
                            initial[f'{day}_end_{i}'] = slot['end']
                        else:
                            # Handle unexpected slot structure
                            initial[f'{day}_start_{i}'] = None
                            initial[f'{day}_end_{i}'] = None
                else:
                    # Handle unexpected slots structure
                    initial[f'{day}_closed'] = True  # Default to closed if structure is unexpected
        return initial

class OpeningHoursDeleteView(DeleteView):
    model = OpeningHours
    template_name = 'opening_hours_confirm_delete.html'
    success_url = reverse_lazy('opening-hours-list')

# Reservation Views
class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservation_list.html'
    context_object_name = 'reservations'

class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservation_detail.html'
    context_object_name = 'reservation'

class ReservationCreateView(CreateView):
    model = Reservation
    template_name = 'reservation_form.html'
    fields = ['restaurant', 'table', 'start_time', 'end_time', 'customer_name', 'customer_email', 'customer_phone', 'party_size', 'reservation_date', 'reservation_time', 'status', 'notes']
    success_url = reverse_lazy('reservation-list')

class ReservationUpdateView(UpdateView):
    model = Reservation
    template_name = 'reservation_form.html'
    fields = ['start_time', 'end_time', 'customer_name', 'customer_email', 'customer_phone', 'party_size', 'reservation_date', 'reservation_time', 'status', 'notes']
    success_url = reverse_lazy('reservation-list')

class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation-list')

# Subscription Views
class SubscriptionListView(ListView):
    model = Subscription
    template_name = 'subscription_list.html'
    context_object_name = 'subscriptions'

class SubscriptionDetailView(DetailView):
    model = Subscription
    template_name = 'subscription_detail.html'
    context_object_name = 'subscription'

class SubscriptionCreateView(CreateView):
    model = Subscription
    template_name = 'subscription_form.html'
    fields = ['customer', 'plan_type', 'start_date', 'end_date', 'status']
    success_url = reverse_lazy('subscription-list')

class SubscriptionUpdateView(UpdateView):
    model = Subscription
    template_name = 'subscription_form.html'
    fields = ['plan_type', 'start_date', 'end_date', 'status']
    success_url = reverse_lazy('subscription-list')

class SubscriptionDeleteView(DeleteView):
    model = Subscription
    template_name = 'subscription_confirm_delete.html'
    success_url = reverse_lazy('subscription-list')

# Billing Views
class BillingListView(ListView):
    model = Billing
    template_name = 'billing_list.html'
    context_object_name = 'billings'

class BillingDetailView(DetailView):
    model = Billing
    template_name = 'billing_detail.html'
    context_object_name = 'billing'

class BillingCreateView(CreateView):
    model = Billing
    template_name = 'billing_form.html'
    fields = ['customer', 'subscription', 'amount', 'date', 'status', 'payment_method']
    success_url = reverse_lazy('billing-list')

class BillingUpdateView(UpdateView):
    model = Billing
    template_name = 'billing_form.html'
    fields = ['amount', 'date', 'status', 'payment_method']
    success_url = reverse_lazy('billing-list')

class BillingDeleteView(DeleteView):
    model = Billing
    template_name = 'billing_confirm_delete.html'
    success_url = reverse_lazy('billing-list')