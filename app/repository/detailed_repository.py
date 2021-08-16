from app import app
from app.models.detailed_model import DetailedReport


class DetailedReportRepository:
    def provider_report(self, filters: dict):
        try:
            report = DetailedReport.provider_report(filters)
            if len(report) == 0:
                return None
            return report
        except Exception as e:
            app.logger.error(e)
            return None
