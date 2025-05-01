from entity.Report import Report
from entity.Booking import Booking
from entity.CleaningService import CleaningService
from entity.UserAccount import User
from datetime import datetime, timedelta
import json
from db_config import db

class ReportBaseController:
    """Base class for report generation controllers"""
    
    @staticmethod
    def save_report(report_type, report_data):
        """Save a new report to the database"""
        try:
            # Create a new report
            report = Report(None, report_type)
            report.reportData = json.dumps(report_data)
            
            # Save to database
            db.session.add(report)
            db.session.commit()
            
            return True, f"{report_type} generated successfully!"
        except Exception as e:
            db.session.rollback()
            print(f"Error saving report: {str(e)}")
            return False, f"Error generating report: {str(e)}"


class GenerateDailyReportController(ReportBaseController):
    """Controller for generating daily reports"""
    
    @classmethod
    def generate_report(cls):
        """Generate a daily report with booking and revenue data"""
        try:
            # Define the time period (today)
            today = datetime.now().date()
            
            # Get bookings for today
            daily_bookings = Booking.get_bookings_by_date_range(today, today)
            
            # Calculate metrics
            total_bookings = len(daily_bookings)
            total_revenue = sum(booking.totalPrice for booking in daily_bookings if booking.totalPrice)
            confirmed_bookings = sum(1 for booking in daily_bookings if booking.bookingStatus == 'Confirmed')
            pending_bookings = sum(1 for booking in daily_bookings if booking.bookingStatus == 'Pending')
            
            # Get service distribution
            service_counts = {}
            for booking in daily_bookings:
                service = CleaningService.find_by_id(booking.serviceID)
                if service:
                    service_title = service.title
                    service_counts[service_title] = service_counts.get(service_title, 0) + 1
            
            # Compile report data
            report_data = {
                'report_date': today.strftime('%Y-%m-%d'),
                'total_bookings': total_bookings,
                'total_revenue': float(total_revenue),
                'confirmed_bookings': confirmed_bookings,
                'pending_bookings': pending_bookings,
                'service_distribution': service_counts
            }
            
            # Save the report
            return cls.save_report('Daily Report', report_data)
            
        except Exception as e:
            print(f"Error generating daily report: {str(e)}")
            return False, f"Error generating daily report: {str(e)}"


class GenerateWeeklyReportController(ReportBaseController):
    """Controller for generating weekly reports"""
    
    @classmethod
    def generate_report(cls):
        """Generate a weekly report with booking and revenue data"""
        try:
            # Define the time period (last 7 days)
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=6)  # 7 days including today
            
            # Get bookings for the week
            weekly_bookings = Booking.get_bookings_by_date_range(start_date, end_date)
            
            # Calculate metrics
            total_bookings = len(weekly_bookings)
            total_revenue = sum(booking.totalPrice for booking in weekly_bookings if booking.totalPrice)
            
            # Calculate daily distribution
            daily_stats = {}
            for i in range(7):
                day = start_date + timedelta(days=i)
                day_str = day.strftime('%Y-%m-%d')
                daily_stats[day_str] = {
                    'bookings': 0,
                    'revenue': 0.0
                }
            
            for booking in weekly_bookings:
                booking_date = booking.bookingDate.strftime('%Y-%m-%d')
                if booking_date in daily_stats:
                    daily_stats[booking_date]['bookings'] += 1
                    daily_stats[booking_date]['revenue'] += float(booking.totalPrice or 0)
            
            # Get cleaner performance
            cleaner_stats = {}
            for booking in weekly_bookings:
                cleaner_id = booking.cleanerID
                if cleaner_id:
                    if cleaner_id not in cleaner_stats:
                        cleaner = User.find_by_id(cleaner_id)
                        cleaner_name = f"{cleaner.profile.first_name} {cleaner.profile.last_name}" if cleaner and cleaner.profile else f"Cleaner {cleaner_id}"
                        cleaner_stats[cleaner_id] = {
                            'name': cleaner_name,
                            'bookings': 0,
                            'revenue': 0.0
                        }
                    cleaner_stats[cleaner_id]['bookings'] += 1
                    cleaner_stats[cleaner_id]['revenue'] += float(booking.totalPrice or 0)
            
            # Compile report data
            report_data = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'total_bookings': total_bookings,
                'total_revenue': float(total_revenue),
                'daily_statistics': daily_stats,
                'cleaner_performance': list(cleaner_stats.values())
            }
            
            # Save the report
            return cls.save_report('Weekly Report', report_data)
            
        except Exception as e:
            print(f"Error generating weekly report: {str(e)}")
            return False, f"Error generating weekly report: {str(e)}"


class GenerateMonthlyReportController(ReportBaseController):
    """Controller for generating monthly reports"""
    
    @classmethod
    def generate_report(cls):
        """Generate a monthly report with booking, revenue and trend data"""
        try:
            # Define the time period (last 30 days)
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=29)  # 30 days including today
            
            # Get bookings for the month
            monthly_bookings = Booking.get_bookings_by_date_range(start_date, end_date)
            
            # Calculate metrics
            total_bookings = len(monthly_bookings)
            total_revenue = sum(booking.totalPrice for booking in monthly_bookings if booking.totalPrice)
            avg_booking_value = total_revenue / total_bookings if total_bookings > 0 else 0
            
            # Calculate weekly trends (divide the month into 4 weeks)
            weekly_trends = []
            for i in range(4):
                week_start = start_date + timedelta(days=i*7)
                week_end = min(week_start + timedelta(days=6), end_date)
                
                week_bookings = [b for b in monthly_bookings if week_start <= b.bookingDate <= week_end]
                week_revenue = sum(booking.totalPrice for booking in week_bookings if booking.totalPrice)
                
                weekly_trends.append({
                    'week': i+1,
                    'start_date': week_start.strftime('%Y-%m-%d'),
                    'end_date': week_end.strftime('%Y-%m-%d'),
                    'bookings': len(week_bookings),
                    'revenue': float(week_revenue)
                })
            
            # Get category performance
            category_stats = {}
            for booking in monthly_bookings:
                service = CleaningService.find_by_id(booking.serviceID)
                if service:
                    category_id = service.categoryID
                    if category_id not in category_stats:
                        from entity.Category import Category
                        category = Category.find_by_id(category_id)
                        category_name = category.name if category else f"Category {category_id}"
                        category_stats[category_id] = {
                            'name': category_name,
                            'bookings': 0,
                            'revenue': 0.0
                        }
                    category_stats[category_id]['bookings'] += 1
                    category_stats[category_id]['revenue'] += float(booking.totalPrice or 0)
            
            # Compile report data
            report_data = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'total_bookings': total_bookings,
                'total_revenue': float(total_revenue),
                'average_booking_value': float(avg_booking_value),
                'weekly_trends': weekly_trends,
                'category_performance': list(category_stats.values())
            }
            
            # Save the report
            return cls.save_report('Monthly Report', report_data)
            
        except Exception as e:
            print(f"Error generating monthly report: {str(e)}")
            return False, f"Error generating monthly report: {str(e)}"