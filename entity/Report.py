from datetime import datetime
import json
from db_config import db

class Report(db.Model):
    __tablename__ = 'REPORT'
    
    reportID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reportType = db.Column(db.String(100))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    reportData = db.Column(db.Text)
    
    
    def __init__(self, platformManagerID, reportType):

        self.reportType = reportType
        self.reportData = None
        
    def to_dict(self):
        data = {
            'reportID': self.reportID,
            'reportType': self.reportType,
            'create_at': self.create_at.isoformat() if self.create_at else None
        }
        
        # Parse and include report data if available
        if self.reportData:
            try:
                data['reportData'] = json.loads(self.reportData)
            except:
                data['reportData'] = self.reportData
        
        return data
    
    @classmethod
    def find_by_id(cls, report_id):
        """Find a report by ID"""
        return cls.query.get(report_id)

    
    @classmethod
    def find_by_type(cls, report_type):
        """Find reports by type"""
        return cls.query.filter_by(reportType=report_type).all()