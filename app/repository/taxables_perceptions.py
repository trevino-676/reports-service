import uuid

from app import app
from app.models import TaxablesPerceptions
from app.repository import ReportRepository


class TaxablesPerceptionsRepository(ReportRepository):
    def get_report(self, filters: dict) -> list:
        try:
            report = TaxablesPerceptions.get_taxables_perceptions(filters)
            if len(report) == 0:
                return None

            for item in report:
                item["uuid"] = uuid.uuid4().hex

            return report
        except Exception as e:
            app.logger.error(e)
            return None
