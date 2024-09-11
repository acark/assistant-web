from typing import Dict, Any, List
from datetime import datetime, time, timedelta
import pytz
from restaurants.models import Restaurant, Table, OpeningHours, Reservation

class RestaurantManager:
    def get_restaurant(self, restaurant_id: int) -> Restaurant:
        return Restaurant.objects.get(id=restaurant_id)

    def validate_booking_datetime(self, restaurant_id: int, booking_datetime: str) -> Dict[str, Any]:
        try:
            restaurant = self.get_restaurant(restaurant_id)
        except Restaurant.DoesNotExist:
            return {"is_valid": False, "reason": "Restaurant not found"}

        try:
            dt = datetime.fromisoformat(booking_datetime)
            tz = pytz.timezone(restaurant.timezone)
            dt = tz.localize(dt)
        except ValueError:
            return {"is_valid": False, "reason": "Invalid datetime format"}

        if dt < datetime.now(tz):
            return {"is_valid": False, "reason": "Booking time is in the past"}

        day_of_week = dt.weekday()
        time = dt.time()
        
        opening_hours = OpeningHours.objects.filter(restaurant=restaurant, day=day_of_week)
        if not any(oh.open_time <= time < oh.close_time for oh in opening_hours):
            return {"is_valid": False, "reason": "Restaurant is closed at this time"}

        return {"is_valid": True}

    def check_restaurant_availability(self, restaurant_id: int, booking_datetime: str, party_size: int, duration: int = 120) -> Dict[str, Any]:
        try:
            restaurant = self.get_restaurant(restaurant_id)
        except Restaurant.DoesNotExist:
            return {"is_available": False, "reason": "Restaurant not found"}

        try:
            dt = datetime.fromisoformat(booking_datetime)
            tz = pytz.timezone(restaurant.timezone)
            dt = tz.localize(dt)
        except ValueError:
            return {"is_available": False, "reason": "Invalid datetime format"}

        validation_result = self.validate_booking_datetime(restaurant_id, booking_datetime)
        if not validation_result["is_valid"]:
            return {"is_available": False, "reason": validation_result["reason"]}

        end_time = dt + timedelta(minutes=duration)
        available_tables = Table.objects.filter(restaurant=restaurant, capacity__gte=party_size).exclude(
            reservations__start_time__lt=end_time,
            reservations__end_time__gt=dt
        )

        if not available_tables:
            return {"is_available": False, "reason": "No available tables for the given party size"}

        return {"is_available": True, "available_tables": available_tables.count()}

    def suggest_alternative_times(self, restaurant_id: int, booking_datetime: str, party_size: int, duration: int = 120, num_suggestions: int = 3) -> Dict[str, Any]:
        try:
            restaurant = self.get_restaurant(restaurant_id)
        except Restaurant.DoesNotExist:
            return {"success": False, "reason": "Restaurant not found"}

        try:
            dt = datetime.fromisoformat(booking_datetime)
            tz = pytz.timezone(restaurant.timezone)
            dt = tz.localize(dt)
        except ValueError:
            return {"success": False, "reason": "Invalid datetime format"}

        suggestions = []
        current_dt = dt
        days_checked = 0

        while len(suggestions) < num_suggestions and days_checked < 7:
            day_of_week = current_dt.weekday()
            opening_hours = OpeningHours.objects.filter(restaurant=restaurant, day=day_of_week)

            for oh in opening_hours:
                current_dt = current_dt.replace(hour=oh.open_time.hour, minute=oh.open_time.minute, second=0, microsecond=0)
                while current_dt.time() < oh.close_time:
                    if current_dt > dt and self.check_restaurant_availability(restaurant_id, current_dt.isoformat(), party_size, duration)["is_available"]:
                        suggestions.append(current_dt.isoformat())
                        if len(suggestions) == num_suggestions:
                            break
                    current_dt += timedelta(minutes=30)
                
                if len(suggestions) == num_suggestions:
                    break

            if len(suggestions) < num_suggestions:
                current_dt = current_dt.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                days_checked += 1

        if not suggestions:
            return {"success": False, "reason": "No alternative times available within the next 7 days"}

        return {
            "success": True,
            "original_request": booking_datetime,
            "alternative_times": suggestions
        }

# Initialize the RestaurantManager
restaurant_manager = RestaurantManager()
