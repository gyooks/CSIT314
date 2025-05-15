from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta
from entity.Booking import Booking
from entity.CleaningService import CleaningService
from db_config import db
from controller.platformManager.GenerateReportController import ReportBaseController


class GenerateMonthlyReportController(ReportBaseController):
    @classmethod
    def generate_report(cls):
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=29)

            monthly_bookings = Booking.get_bookings_by_date_range(start_date, end_date)
            total_bookings = len(monthly_bookings)
            total_revenue = sum(b.totalPrice for b in monthly_bookings if b.totalPrice)
            avg_value = total_revenue / total_bookings if total_bookings else 0
            
            # Track all four booking statuses
            status_counts = {
                'Pending': sum(1 for b in monthly_bookings if b.bookingStatus == 'Pending'),
                'Confirmed': sum(1 for b in monthly_bookings if b.bookingStatus == 'Confirmed'),
                'Completed': sum(1 for b in monthly_bookings if b.bookingStatus == 'Completed'),
                'Cancelled': sum(1 for b in monthly_bookings if b.bookingStatus == 'Cancelled')
            }
            
            # Calculate completion rate
            eligible_bookings = status_counts['Completed'] + status_counts['Cancelled']
            completion_rate = (status_counts['Completed'] / eligible_bookings) * 100 if eligible_bookings > 0 else 0

            weekly_trends = []
            for i in range(4):
                ws = start_date + timedelta(days=i*7)
                we = min(ws + timedelta(days=6), end_date)
                bookings = [b for b in monthly_bookings if ws <= b.bookingDate <= we]
                revenue = sum(b.totalPrice for b in bookings if b.totalPrice)
                weekly_trends.append({'week': i+1, 'start_date': ws.strftime('%Y-%m-%d'), 'end_date': we.strftime('%Y-%m-%d'), 'bookings': len(bookings), 'revenue': float(revenue)})

            category_stats = {}
            for b in monthly_bookings:
                s = CleaningService.find_by_id(b.serviceID)
                if s:
                    cid = s.categoryID
                    if cid not in category_stats:
                        from entity.Category import Category
                        cat = Category.find_by_id(cid)
                        name = cat.name if cat else f"Category {cid}"
                        category_stats[cid] = {'name': name, 'bookings': 0, 'revenue': 0.0}
                    category_stats[cid]['bookings'] += 1
                    category_stats[cid]['revenue'] += float(b.totalPrice or 0)

            # --- ML Prediction for Next Month Bookings ---
            prev_months = []
            for i in range(4, 0, -1):
                start = start_date - timedelta(days=30*i)
                end = start + timedelta(days=29)
                count = len(Booking.get_bookings_by_date_range(start, end))
                prev_months.append(count)

            X = np.array(range(4)).reshape(-1, 1)
            y = np.array(prev_months)
            model = LinearRegression().fit(X, y)
            predicted_next_month = int(model.predict(np.array([[4]]))[0])

            report_data = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'total_bookings': total_bookings,
                'total_revenue': float(total_revenue),
                'average_booking_value': float(avg_value),
                'booking_status': status_counts,
                'completion_rate': float(completion_rate),
                'weekly_trends': weekly_trends,
                'category_performance': list(category_stats.values()),
                'predicted_next_month_bookings': predicted_next_month
            }

            return cls.save_report('Monthly Report', report_data)

        except Exception as e:
            print(f"Error generating monthly report: {str(e)}")
            return False, f"Error generating monthly report: {str(e)}"