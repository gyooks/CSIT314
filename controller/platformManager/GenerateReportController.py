from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta
from entity.Report import Report
from entity.Booking import Booking
from entity.CleaningService import CleaningService
from entity.UserAccount import User
from db_config import db
import json

class ReportBaseController:
    @staticmethod
    def save_report(report_type, report_data):
        try:
            report = Report(None, report_type)
            report.reportData = json.dumps(report_data)
            db.session.add(report)
            db.session.commit()
            return True, f"{report_type} generated successfully!"
        except Exception as e:
            db.session.rollback()
            print(f"Error saving report: {str(e)}")
            return False, f"Error generating report: {str(e)}"


class GenerateDailyReportController(ReportBaseController):
    @classmethod
    def generate_report(cls):
        try:
            today = datetime.now().date()
            daily_bookings = Booking.get_bookings_by_date_range(today, today)

            total_bookings = len(daily_bookings)
            total_revenue = sum(booking.totalPrice for booking in daily_bookings if booking.totalPrice)
            confirmed_bookings = sum(1 for booking in daily_bookings if booking.bookingStatus == 'Confirmed')
            pending_bookings = sum(1 for booking in daily_bookings if booking.bookingStatus == 'Pending')

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

            report_data = {
                'report_date': today.strftime('%Y-%m-%d'),
                'total_bookings': total_bookings,
                'total_revenue': float(total_revenue),
                'confirmed_bookings': confirmed_bookings,
                'pending_bookings': pending_bookings,
                'service_distribution': service_counts,
                'predicted_next_day_bookings': predicted_booking
            }

            return cls.save_report('Daily Report', report_data)

        except Exception as e:
            print(f"Error generating daily report: {str(e)}")
            return False, f"Error generating daily report: {str(e)}"


class GenerateWeeklyReportController(ReportBaseController):
    @classmethod
    def generate_report(cls):
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=6)

            weekly_bookings = Booking.get_bookings_by_date_range(start_date, end_date)

            total_bookings = len(weekly_bookings)
            total_revenue = sum(b.totalPrice for b in weekly_bookings if b.totalPrice)

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
                        name = f"{cleaner.profile.first_name} {cleaner.profile.last_name}" if cleaner and cleaner.profile else f"Cleaner {cid}"
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

            report_data = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'total_bookings': total_bookings,
                'total_revenue': float(total_revenue),
                'daily_statistics': daily_stats,
                'cleaner_performance': list(cleaner_stats.values()),
                'predicted_next_week_bookings': predicted_next_week
            }

            return cls.save_report('Weekly Report', report_data)

        except Exception as e:
            print(f"Error generating weekly report: {str(e)}")
            return False, f"Error generating weekly report: {str(e)}"


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
                'weekly_trends': weekly_trends,
                'category_performance': list(category_stats.values()),
                'predicted_next_month_bookings': predicted_next_month
            }

            return cls.save_report('Monthly Report', report_data)

        except Exception as e:
            print(f"Error generating monthly report: {str(e)}")
            return False, f"Error generating monthly report: {str(e)}"