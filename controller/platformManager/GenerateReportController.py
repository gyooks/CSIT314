import json
from datetime import datetime, timedelta
from sqlalchemy import func, and_, extract
from entity.Report import Report
from entity.Booking import Booking
from entity.CleaningService import CleaningService
from entity.Category import Category
from entity.UserAccount import User
from db_config import db

class BaseReportController:
    """Base controller class for report generation"""
    
    def _create_report(self, platform_manager_id, report_type, report_data):
        """Create a new report entity"""
        try:
            # Check if platform manager exists
            platform_manager = User.query.filter_by(userID=platform_manager_id, role='Platform manager').first()
            if not platform_manager:
                return None
            
            # Create report
            report = Report(platform_manager_id, report_type)
            report.reportData = json.dumps(report_data)
            
            # Save to database
            db.session.add(report)
            db.session.commit()
            
            return report
        except Exception as e:
            db.session.rollback()
            print(f"Error creating report: {str(e)}")
            return None


class DailyReportController(BaseReportController):
    """Controller for generating daily reports"""
    
    def generate_report(self, platform_manager_id, date_str):
        """Generate a daily report for the given date"""
        try:
            # Convert string date to datetime object
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Get all bookings for the specified date
            bookings = Booking.query.filter(
                func.date(Booking.bookingDate) == target_date
            ).all()
            
            # Calculate total revenue
            total_revenue = sum(booking.totalPrice for booking in bookings)
            
            # Count bookings by status
            status_counts = {}
            for booking in bookings:
                status = booking.bookingStatus
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Get service categories used
            services_used = {}
            for booking in bookings:
                service = CleaningService.query.get(booking.serviceID)
                if service:
                    category = Category.query.get(service.categoryID)
                    if category:
                        services_used[category.name] = services_used.get(category.name, 0) + 1
            
            # Compile report data
            report_data = {
                'date': date_str,
                'total_bookings': len(bookings),
                'total_revenue': float(total_revenue),
                'bookings_by_status': status_counts,
                'services_by_category': services_used,
                'generated_at': datetime.now().isoformat()
            }
            
            # Create report entity
            return self._create_report(platform_manager_id, 'Daily', report_data)
            
        except Exception as e:
            print(f"Error generating daily report: {str(e)}")
            return None


class WeeklyReportController(BaseReportController):
    """Controller for generating weekly reports"""
    
    def generate_report(self, platform_manager_id, start_date_str, end_date_str):
        """Generate a weekly report for the given date range"""
        try:
            # Convert string dates to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            # Validate that end_date is after start_date
            if end_date < start_date:
                raise ValueError("End date must be after start date")
            
            # Get all bookings for the specified date range
            bookings = Booking.query.filter(
                and_(
                    func.date(Booking.bookingDate) >= start_date,
                    func.date(Booking.bookingDate) <= end_date
                )
            ).all()
            
            # Calculate total revenue
            total_revenue = sum(booking.totalPrice for booking in bookings)
            
            # Calculate daily averages
            days_in_range = (end_date - start_date).days + 1
            avg_bookings_per_day = len(bookings) / days_in_range if days_in_range > 0 else 0
            avg_revenue_per_day = total_revenue / days_in_range if days_in_range > 0 else 0
            
            # Count bookings by status
            status_counts = {}
            for booking in bookings:
                status = booking.bookingStatus
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Get service categories used
            services_used = {}
            for booking in bookings:
                service = CleaningService.query.get(booking.serviceID)
                if service:
                    category = Category.query.get(service.categoryID)
                    if category:
                        services_used[category.name] = services_used.get(category.name, 0) + 1
            
            # Get most active cleaners
            cleaner_bookings = {}
            for booking in bookings:
                cleaner_id = booking.cleanerID
                cleaner_bookings[cleaner_id] = cleaner_bookings.get(cleaner_id, 0) + 1
            
            top_cleaners = []
            for cleaner_id, count in sorted(cleaner_bookings.items(), key=lambda x: x[1], reverse=True)[:5]:
                cleaner = User.query.get(cleaner_id)
                if cleaner:
                    top_cleaners.append({
                        'cleaner_id': cleaner_id,
                        'email': cleaner.email,
                        'bookings_count': count
                    })
            
            # Compile report data
            report_data = {
                'start_date': start_date_str,
                'end_date': end_date_str,
                'days_in_period': days_in_range,
                'total_bookings': len(bookings),
                'total_revenue': float(total_revenue),
                'avg_bookings_per_day': float(avg_bookings_per_day),
                'avg_revenue_per_day': float(avg_revenue_per_day),
                'bookings_by_status': status_counts,
                'services_by_category': services_used,
                'top_cleaners': top_cleaners,
                'generated_at': datetime.now().isoformat()
            }
            
            # Create report entity
            return self._create_report(platform_manager_id, 'Weekly', report_data)
            
        except Exception as e:
            print(f"Error generating weekly report: {str(e)}")
            return None


class MonthlyReportController(BaseReportController):
    """Controller for generating monthly reports"""
    
    def generate_report(self, platform_manager_id, year, month):
        """Generate a monthly report for the given year and month"""
        try:
            # Convert year and month to integers
            year = int(year)
            month = int(month)
            
            # Validate month
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12")
            
            # Get all bookings for the specified month and year
            bookings = Booking.query.filter(
                and_(
                    extract('year', Booking.bookingDate) == year,
                    extract('month', Booking.bookingDate) == month
                )
            ).all()
            
            # Calculate total revenue
            total_revenue = sum(booking.totalPrice for booking in bookings)
            
            # Calculate daily averages for the month
            import calendar
            days_in_month = calendar.monthrange(year, month)[1]
            avg_bookings_per_day = len(bookings) / days_in_month if days_in_month > 0 else 0
            avg_revenue_per_day = total_revenue / days_in_month if days_in_month > 0 else 0
            
            # Count bookings by status
            status_counts = {}
            for booking in bookings:
                status = booking.bookingStatus
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Get service categories used
            services_used = {}
            for booking in bookings:
                service = CleaningService.query.get(booking.serviceID)
                if service:
                    category = Category.query.get(service.categoryID)
                    if category:
                        services_used[category.name] = services_used.get(category.name, 0) + 1
            
            # Get most active cleaners
            cleaner_bookings = {}
            for booking in bookings:
                cleaner_id = booking.cleanerID
                cleaner_bookings[cleaner_id] = cleaner_bookings.get(cleaner_id, 0) + 1
            
            top_cleaners = []
            for cleaner_id, count in sorted(cleaner_bookings.items(), key=lambda x: x[1], reverse=True)[:5]:
                cleaner = User.query.get(cleaner_id)
                if cleaner:
                    top_cleaners.append({
                        'cleaner_id': cleaner_id,
                        'email': cleaner.email,
                        'bookings_count': count
                    })
            
            # Get most active customers
            customer_bookings = {}
            for booking in bookings:
                customer_id = booking.homeownerID
                customer_bookings[customer_id] = customer_bookings.get(customer_id, 0) + 1
            
            top_customers = []
            for customer_id, count in sorted(customer_bookings.items(), key=lambda x: x[1], reverse=True)[:5]:
                customer = User.query.get(customer_id)
                if customer:
                    top_customers.append({
                        'customer_id': customer_id,
                        'email': customer.email,
                        'bookings_count': count
                    })
            
            # Month name
            month_name = calendar.month_name[month]
            
            # Compile report data
            report_data = {
                'year': year,
                'month': month,
                'month_name': month_name,
                'days_in_month': days_in_month,
                'total_bookings': len(bookings),
                'total_revenue': float(total_revenue),
                'avg_bookings_per_day': float(avg_bookings_per_day),
                'avg_revenue_per_day': float(avg_revenue_per_day),
                'bookings_by_status': status_counts,
                'services_by_category': services_used,
                'top_cleaners': top_cleaners,
                'top_customers': top_customers,
                'generated_at': datetime.now().isoformat()
            }
            
            # Create report entity
            return self._create_report(platform_manager_id, 'Monthly', report_data)
            
        except Exception as e:
            print(f"Error generating monthly report: {str(e)}")
            return None


class YearlyReportController(BaseReportController):
    """Controller for generating yearly reports"""
    
    def generate_report(self, platform_manager_id, year):
        """Generate a yearly report for the given year"""
        try:
            # Convert year to integer
            year = int(year)
            
            # Get all bookings for the specified year
            bookings = Booking.query.filter(
                extract('year', Booking.bookingDate) == year
            ).all()
            
            # Calculate total revenue
            total_revenue = sum(booking.totalPrice for booking in bookings)
            
            # Calculate monthly breakdown
            monthly_data = {}
            for month in range(1, 13):
                month_bookings = [b for b in bookings if b.bookingDate.month == month]
                monthly_revenue = sum(booking.totalPrice for booking in month_bookings)
                monthly_data[month] = {
                    'month_name': datetime(year, month, 1).strftime('%B'),
                    'bookings_count': len(month_bookings),
                    'revenue': float(monthly_revenue)
                }
            
            # Count bookings by status
            status_counts = {}
            for booking in bookings:
                status = booking.bookingStatus
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Get service categories used
            services_used = {}
            for booking in bookings:
                service = CleaningService.query.get(booking.serviceID)
                if service:
                    category = Category.query.get(service.categoryID)
                    if category:
                        services_used[category.name] = services_used.get(category.name, 0) + 1
            
            # Get most active cleaners
            cleaner_bookings = {}
            for booking in bookings:
                cleaner_id = booking.cleanerID
                cleaner_bookings[cleaner_id] = cleaner_bookings.get(cleaner_id, 0) + 1
            
            top_cleaners = []
            for cleaner_id, count in sorted(cleaner_bookings.items(), key=lambda x: x[1], reverse=True)[:10]:
                cleaner = User.query.get(cleaner_id)
                if cleaner:
                    top_cleaners.append({
                        'cleaner_id': cleaner_id,
                        'email': cleaner.email,
                        'bookings_count': count
                    })
            
            # Get most active customers
            customer_bookings = {}
            for booking in bookings:
                customer_id = booking.homeownerID
                customer_bookings[customer_id] = customer_bookings.get(customer_id, 0) + 1
            
            top_customers = []
            for customer_id, count in sorted(customer_bookings.items(), key=lambda x: x[1], reverse=True)[:10]:
                customer = User.query.get(customer_id)
                if customer:
                    top_customers.append({
                        'customer_id': customer_id,
                        'email': customer.email,
                        'bookings_count': count
                    })
            
            # Calculate growth (compare with previous year if available)
            prev_year_bookings = Booking.query.filter(
                extract('year', Booking.bookingDate) == year - 1
            ).all()
            
            prev_year_revenue = sum(booking.totalPrice for booking in prev_year_bookings)
            revenue_growth = ((total_revenue - prev_year_revenue) / prev_year_revenue * 100) if prev_year_revenue > 0 else None
            
            bookings_growth = ((len(bookings) - len(prev_year_bookings)) / len(prev_year_bookings) * 100) if len(prev_year_bookings) > 0 else None
            
            # Compile report data
            report_data = {
                'year': year,
                'total_bookings': len(bookings),
                'total_revenue': float(total_revenue),
                'monthly_breakdown': monthly_data,
                'bookings_growth': float(bookings_growth) if bookings_growth is not None else None,
                'revenue_growth': float(revenue_growth) if revenue_growth is not None else None,
                'bookings_by_status': status_counts,
                'services_by_category': services_used,
                'top_cleaners': top_cleaners,
                'top_customers': top_customers,
                'generated_at': datetime.now().isoformat()
            }
            
            # Create report entity
            return self._create_report(platform_manager_id, 'Yearly', report_data)
            
        except Exception as e:
            print(f"Error generating yearly report: {str(e)}")
            return None