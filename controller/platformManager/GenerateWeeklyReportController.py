from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta
from entity.Booking import Booking
from entity.UserAccount import User
from db_config import db
from controller.platformManager.GenerateReportController import ReportBaseController


class GenerateWeeklyReportController(ReportBaseController):
    @classmethod
    def generate_report(cls):
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=6)

            weekly_bookings = Booking.get_bookings_by_date_range(start_date, end_date)
            
            total_bookings = len(weekly_bookings)
            total_revenue = sum(b.totalPrice for b in weekly_bookings if b.totalPrice)
            
            # Track all four booking statuses
            status_counts = {
                'Pending': sum(1 for b in weekly_bookings if b.bookingStatus == 'Pending'),
                'Confirmed': sum(1 for b in weekly_bookings if b.bookingStatus == 'Confirmed'),
                'Completed': sum(1 for b in weekly_bookings if b.bookingStatus == 'Completed'),
                'Cancelled': sum(1 for b in weekly_bookings if b.bookingStatus == 'Cancelled')
            }

            daily_stats = { (start_date + timedelta(days=i)).strftime('%Y-%m-%d'): {'bookings': 0, 'revenue': 0.0} for i in range(7) }
            for b in weekly_bookings:
                day = b.bookingDate.strftime('%Y-%m-%d')
                if day in daily_stats:
                    daily_stats[day]['bookings'] += 1
                    daily_stats[day]['revenue'] += float(b.totalPrice or 0)

            cleaner_stats = {}
            for b in weekly_bookings:
                cid = b.cleanerID
                if cid:
                    if cid not in cleaner_stats:
                        cleaner = User.find_by_id(cid)
                        profile = cleaner.profile
                        fname = cleaner.first_name or ""
                        lname = cleaner.last_name or ""
                        name = f"{fname} {lname}".strip() or f"Cleaner {cid}"
                        cleaner_stats[cid] = {'name': name, 'bookings': 0, 'revenue': 0.0}
                    cleaner_stats[cid]['bookings'] += 1
                    cleaner_stats[cid]['revenue'] += float(b.totalPrice or 0)

            # --- ML Prediction for Next Week Bookings ---
            previous_weeks = []
            for i in range(4, 0, -1):
                week_start = start_date - timedelta(days=7*i)
                week_end = week_start + timedelta(days=6)
                count = len(Booking.get_bookings_by_date_range(week_start, week_end))
                previous_weeks.append(count)

            X = np.array(range(4)).reshape(-1, 1)
            y = np.array(previous_weeks)
            model = LinearRegression().fit(X, y)
            predicted_next_week = int(model.predict(np.array([[4]]))[0])

            prev_week_start = start_date - timedelta(days=7)
            prev_week_end = start_date - timedelta(days=1)
            prev_week_bookings = Booking.get_bookings_by_date_range(prev_week_start, prev_week_end)

            report_data = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'total_bookings': total_bookings,
                'total_revenue': float(total_revenue),
                'booking_status': status_counts,
                'daily_statistics': daily_stats,
                'cleaner_performance': list(cleaner_stats.values()),
                'predicted_next_week_bookings': predicted_next_week,
                'previous_week_bookings': len(prev_week_bookings)
            }

            return cls.save_report('Weekly Report', report_data)

        except Exception as e:
            print(f"Error generating weekly report: {str(e)}")
            return False, f"Error generating weekly report: {str(e)}"