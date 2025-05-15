import numpy as np
from entity.Report import Report
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