from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from entity.Report import Report
from controller.platformManager.GenerateReportController import ReportBaseController
from controller.platformManager.GenerateDailyReportController import GenerateDailyReportController
from controller.platformManager.GenerateWeeklyReportController import GenerateWeeklyReportController
from controller.platformManager.GenerateMonthlyReportController import GenerateMonthlyReportController
import json

# Create the blueprint
reportManagementUI_bp = Blueprint('reportManagementUI', __name__, url_prefix='/platform-manager')

@reportManagementUI_bp.route('/reports', methods=['GET'])
def manage_reports():
    """Display the report management page"""
    # Check if user is logged in and is a platform manager
    if 'user_id' not in session:
        flash("You must be logged in to access this page", "error")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Get all reports
    reports = Report.query.order_by(Report.reportID.desc()).all()
    
    return render_template('platformManager/reportManagementPage.html', reports=reports)

@reportManagementUI_bp.route('/generate-report', methods=['POST'])
def generate_report():
    """Generate a new report based on the selected type"""
    # Check if user is logged in and is a platform manager
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'You must be logged in to perform this action'}), 401
    
    # Get the report type from the form
    report_type = request.form.get('report_type')
    
    if not report_type:
        flash('Please select a report type', 'error')
        return redirect(url_for('reportManagementUI.manage_reports'))
    
    # Generate the report based on the selected type
    success = False
    message = ''
    
    if report_type == 'daily':
        success, message = GenerateDailyReportController.generate_report()
    elif report_type == 'weekly':
        success, message = GenerateWeeklyReportController.generate_report()
    elif report_type == 'monthly':
        success, message = GenerateMonthlyReportController.generate_report()
    else:
        message = 'Invalid report type selected'
    
    # Return to the report management page with appropriate message
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('reportManagementUI.manage_reports'))

@reportManagementUI_bp.route('/view-report/<int:report_id>', methods=['GET'])
def view_report(report_id):
    """View a specific report"""
    # Check if user is logged in and is a platform manager
    if 'user_id' not in session:
        flash("You must be logged in to access this page", "error")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Get the report
    report = Report.find_by_id(report_id)
    
    if not report:
        flash('Report not found', 'error')
        return redirect(url_for('reportManagementUI.manage_reports'))
    
    # Parse the report data
    report_data = None
    if report.reportData:
        try:
            report_data = json.loads(report.reportData)
        except Exception as e:
            flash(f'Error parsing report data: {str(e)}', 'error')
            return redirect(url_for('reportManagementUI.manage_reports'))
    
    return render_template('platformManager/viewReportPage.html', report=report, report_data=report_data)

@reportManagementUI_bp.route('/delete-report/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    """Delete a report"""
    # Check if user is logged in and is a platform manager
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "error")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Get the report
    report = Report.find_by_id(report_id)
    
    if not report:
        flash('Report not found', 'error')
        return redirect(url_for('reportManagementUI.manage_reports'))
    
    try:
        # Delete the report
        report.delete_from_db()
        flash('Report deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting report: {str(e)}', 'error')
    
    return redirect(url_for('reportManagementUI.manage_reports'))