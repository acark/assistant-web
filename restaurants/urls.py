from django.urls import path

from restaurants import views

urlpatterns = [
    # Customer URLs
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer-create'),
    path('customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer-update'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer-delete'),

    # Restaurant URLs
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurants/create/', views.RestaurantCreateView.as_view(), name='restaurant-create'),
    path('restaurants/<int:pk>/update/', views.RestaurantUpdateView.as_view(), name='restaurant-update'),
    path('restaurants/<int:pk>/delete/', views.RestaurantDeleteView.as_view(), name='restaurant-delete'),

    # Table URLs
    path('tables/', views.TableListView.as_view(), name='table-list'),
    path('tables/<int:pk>/', views.TableDetailView.as_view(), name='table-detail'),
    path('tables/create/', views.TableCreateView.as_view(), name='table-create'),
    path('tables/<int:pk>/update/', views.TableUpdateView.as_view(), name='table-update'),
    path('tables/<int:pk>/delete/', views.TableDeleteView.as_view(), name='table-delete'),

    # OpeningHours URLs
    path('opening-hours/', views.OpeningHoursListView.as_view(), name='opening-hours-list'),
    path('opening-hours/<int:pk>/', views.OpeningHoursDetailView.as_view(), name='opening-hours-detail'),
    path('opening-hours/create/', views.OpeningHoursCreateView.as_view(), name='opening-hours-create'),
    path('opening-hours/<int:pk>/update/', views.OpeningHoursUpdateView.as_view(), name='opening-hours-update'),
    path('opening-hours/<int:pk>/delete/', views.OpeningHoursDeleteView.as_view(), name='opening-hours-delete'),

    # Reservation URLs
    path('reservations/', views.ReservationListView.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservations/create/', views.ReservationCreateView.as_view(), name='reservation-create'),
    path('reservations/<int:pk>/update/', views.ReservationUpdateView.as_view(), name='reservation-update'),
    path('reservations/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation-delete'),

    # Subscription URLs
    path('subscriptions/', views.SubscriptionListView.as_view(), name='subscription-list'),
    path('subscriptions/<int:pk>/', views.SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('subscriptions/create/', views.SubscriptionCreateView.as_view(), name='subscription-create'),
    path('subscriptions/<int:pk>/update/', views.SubscriptionUpdateView.as_view(), name='subscription-update'),
    path('subscriptions/<int:pk>/delete/', views.SubscriptionDeleteView.as_view(), name='subscription-delete'),

    # Billing URLs
    path('billings/', views.BillingListView.as_view(), name='billing-list'),
    path('billings/<int:pk>/', views.BillingDetailView.as_view(), name='billing-detail'),
    path('billings/create/', views.BillingCreateView.as_view(), name='billing-create'),
    path('billings/<int:pk>/update/', views.BillingUpdateView.as_view(), name='billing-update'),
    path('billings/<int:pk>/delete/', views.BillingDeleteView.as_view(), name='billing-delete'),
]