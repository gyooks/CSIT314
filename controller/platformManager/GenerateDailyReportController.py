from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta
from entity.Report import Report
from entity.Booking import Booking
from entity.CleaningService import CleaningService
from entity.UserAccount import User
from db_config import db
from controller.platformManager.GenerateReportController import ReportBaseController
import json

class GenerateDailyReportController(ReportBaseController):
    @classmethod
    def generate_report(cls):
        try:
            today = datetime.now().date()
            daily_bookings = Booking.get_bookings_by_date_range(today, today)

            total_bookings = len(daily_bookings)
            total_revenue = sum(booking.totalPrice for booking in daily_bookings if booking.totalPrice)
            
            # Track all four booking statuses
            confirmed_bookings = sum(1 for booking in daily_bookings if booking.bookingStatus == 'Confirmed')
            pending_bookings = sum(1 for booking in daily_bookings if booking.bookingStatus == 'Pending')
            completed_bookings = sum(1 for booking in daily_bookings if booking.bookingStatus == 'Completed')
            cancelled_bookings = sum(1 for booking in daily_bookings if booking.bookingStatus == 'Cancelled')
            
            service_counts = {}
            for booking in daily_bookings:
                service = CleaningService.find_by_id(booking.serviceID)
                if service:
                    title = service.title
                    service_counts[title] = service_counts.get(title, 0) + 1

            # --- ML Prediction for Next Day Bookings ---
            past_days = [today - timedelta(days=i) for i in range(1, 8)][::-1]
            booking_counts = [len(Booking.get_bookings_by_date_range(day, day)) for day in past_days]

            X = np.array(range(7)).reshape(-1, 1)
            y = np.array(booking_counts)
            model = LinearRegression().fit(X, y)
            predicted_booking = int(model.predict(np.array([[7]]))[0])

            revenue_series = []
            for day in past_days:
                bookings = Booking.get_bookings_by_date_range(day, day)
                total = sum(b.totalPrice for b in bookings if b.totalPrice)
                revenue_series.append(total)

            X = np.array(range(7)).reshape(-1, 1)
            y_rev = np.array(revenue_series)
            rev_model = LinearRegression().fit(X, y_rev)
            predicted_revenue = float(rev_model.predict(np.array([[7]]))[0])


            report_data = {
                'report_date': today.strftime('%Y-%m-%d'),
                'total_bookings': total_bookings,
                'total_revenue': float(total_revenue),
                'pending_bookings': pending_bookings,
                'confirmed_bookings': confirmed_bookings,
                'completed_bookings': completed_bookings,
                'cancelled_bookings': cancelled_bookings,
                'service_distribution': service_counts,
                'predicted_next_day_bookings': predicted_booking,
                'predicted_next_day_revenue' : predicted_revenue
            }

            return cls.save_report('Daily Report', report_data)
        
        except Exception as e:
            print(f"Error generating daily report: {str(e)}")
            return False, f"Error generating daily report: {str(e)}"
